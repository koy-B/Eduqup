from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_services.gemini_service import AIService
from chat.models import ChatSession, Message

from .serializers import DocumentUploadSerializer
from .services import extract_text_from_file


class DocumentUploadView(APIView):
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = serializer.save(user=request.user)
        extracted_text = extract_text_from_file(document.file.path)
        document.extracted_text = extracted_text
        document.save(update_fields=["extracted_text"])

        ai_service = AIService()
        quiz = ai_service.generate_quiz_from_text(extracted_text)

        session = ChatSession.objects.filter(user=request.user).order_by("-created_at").first()
        if not session:
            session = ChatSession.objects.create(user=request.user, title="Document Analysis Session")

        assistant_text = f"Document analyzed. Here are practice questions:\n{quiz}"
        Message.objects.create(chat_session=session, role="assistant", content=assistant_text)

        return Response(
            {
                "document": DocumentUploadSerializer(document).data,
                "quiz": quiz,
                "chat_session_id": session.id,
            },
            status=status.HTTP_201_CREATED,
        )
