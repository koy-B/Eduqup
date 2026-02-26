from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_services.gemini_service import AIService
from documents.models import Document

from .models import ChatSession, Message
from .permissions import FreeTierMessageLimitPermission
from .serializers import ChatSessionSerializer, SendMessageSerializer, MessageSerializer


class ChatSessionCreateView(APIView):
    def post(self, request):
        serializer = ChatSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save(user=request.user)
        return Response(ChatSessionSerializer(session).data, status=status.HTTP_201_CREATED)


class ChatSessionListView(APIView):
    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by("-created_at")
        return Response(ChatSessionSerializer(sessions, many=True).data, status=status.HTTP_200_OK)


class SendMessageView(APIView):
    permission_classes = [FreeTierMessageLimitPermission]

    def post(self, request, session_id: int):
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data["content"]

        Message.objects.create(chat_session=session, role="user", content=user_message)

        # Include the latest uploaded document text as optional learning context.
        latest_doc = Document.objects.filter(user=request.user).order_by("-uploaded_at").first()
        context_text = latest_doc.extracted_text if latest_doc else ""

        ai_service = AIService()
        assistant_reply = ai_service.generate_response(user_message, context=context_text)

        assistant_msg = Message.objects.create(chat_session=session, role="assistant", content=assistant_reply)
        return Response(MessageSerializer(assistant_msg).data, status=status.HTTP_201_CREATED)
