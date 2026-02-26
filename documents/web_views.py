from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from ai_services.gemini_service import AIService
from chat.models import ChatSession, Message

from .serializers import DocumentUploadSerializer
from .services import extract_text_from_file


@method_decorator(login_required, name="dispatch")
class DocumentUploadPageView(View):
    template_name = "documents/upload.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        serializer = DocumentUploadSerializer(data={"file": request.FILES.get("file")})
        if not serializer.is_valid():
            for field_errors in serializer.errors.values():
                for err in field_errors:
                    messages.error(request, str(err))
            return render(request, self.template_name)

        document = serializer.save(user=request.user)
        extracted_text = extract_text_from_file(document.file.path)
        document.extracted_text = extracted_text
        document.save(update_fields=["extracted_text"])

        ai_service = AIService()
        quiz = ai_service.generate_quiz_from_text(extracted_text)
        session = ChatSession.objects.filter(user=request.user).order_by("-created_at").first()
        if not session:
            session = ChatSession.objects.create(user=request.user, title="Document Analysis Session")
        Message.objects.create(
            chat_session=session,
            role="assistant",
            content=f"Document analyzed. Here are practice questions:\n{quiz}",
        )
        messages.success(request, "Document uploaded and analyzed.")
        return redirect("web-chat-session-detail", session_id=session.id)


@method_decorator(login_required, name="dispatch")
class DocumentUploadApiView(View):
    def post(self, request):
        serializer = DocumentUploadSerializer(data={"file": request.FILES.get("file")})
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        document = serializer.save(user=request.user)
        extracted_text = extract_text_from_file(document.file.path)
        document.extracted_text = extracted_text
        document.save(update_fields=["extracted_text"])

        ai_service = AIService()
        quiz = ai_service.generate_quiz_from_text(extracted_text)
        session = ChatSession.objects.filter(user=request.user).order_by("-created_at").first()
        if not session:
            session = ChatSession.objects.create(user=request.user, title="Document Analysis Session")

        assistant_msg = Message.objects.create(
            chat_session=session,
            role="assistant",
            content=f"Document analyzed. Here are practice questions:\n{quiz}",
        )
        return JsonResponse(
            {
                "document": {
                    "id": document.id,
                    "name": document.file.name,
                    "uploaded_at": document.uploaded_at.isoformat(),
                },
                "session_id": session.id,
                "assistant_message": {
                    "id": assistant_msg.id,
                    "role": assistant_msg.role,
                    "content": assistant_msg.content,
                    "timestamp": assistant_msg.timestamp.isoformat(),
                },
                "quiz": quiz,
            },
            status=201,
        )
