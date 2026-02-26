from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
import json

from ai_services.gemini_service import AIService
from documents.models import Document

from .models import ChatSession, Message


def _free_tier_limit_reached(user) -> bool:
    if user.is_pro:
        return False
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    count = Message.objects.filter(
        chat_session__user=user,
        role="user",
        timestamp__gte=start_of_day,
    ).count()
    return count >= settings.FREE_DAILY_MESSAGE_LIMIT


@method_decorator(login_required, name="dispatch")
class ChatSessionCreatePageView(View):
    def post(self, request):
        session = ChatSession.objects.create(user=request.user, title=request.POST.get("title", "").strip())
        return redirect("web-chat-session-detail", session_id=session.id)


@method_decorator(login_required, name="dispatch")
class ChatSessionDetailView(View):
    template_name = "chat/session_detail.html"

    def get(self, request, session_id: int):
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        return render(
            request,
            self.template_name,
            {"session": session, "messages_list": session.messages.all().order_by("timestamp")},
        )

    def post(self, request, session_id: int):
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        content = request.POST.get("content", "").strip()
        if not content:
            messages.error(request, "Message cannot be empty.")
            return redirect("web-chat-session-detail", session_id=session.id)
        if _free_tier_limit_reached(request.user):
            messages.error(request, "Free daily message limit reached. Upgrade to Pro.")
            return redirect("web-chat-session-detail", session_id=session.id)

        Message.objects.create(chat_session=session, role="user", content=content)
        latest_doc = Document.objects.filter(user=request.user).order_by("-uploaded_at").first()
        context_text = latest_doc.extracted_text if latest_doc else ""
        ai_service = AIService()
        reply = ai_service.generate_response(content, context=context_text)
        Message.objects.create(chat_session=session, role="assistant", content=reply)
        return redirect("web-chat-session-detail", session_id=session.id)


@method_decorator(login_required, name="dispatch")
class ChatSessionListApiView(View):
    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by("-created_at")
        data = [
            {
                "id": session.id,
                "title": session.title or "Untitled Session",
                "created_at": session.created_at.isoformat(),
            }
            for session in sessions
        ]
        return JsonResponse({"sessions": data}, status=200)


@method_decorator(login_required, name="dispatch")
class ChatSessionCreateApiView(View):
    def post(self, request):
        title = ""
        if request.content_type and "application/json" in request.content_type:
            try:
                payload = json.loads(request.body.decode("utf-8")) if request.body else {}
            except json.JSONDecodeError:
                payload = {}
            title = (payload.get("title") or "").strip()
        else:
            title = request.POST.get("title", "").strip()
        session = ChatSession.objects.create(user=request.user, title=title)
        return JsonResponse(
            {
                "id": session.id,
                "title": session.title or "Untitled Session",
                "created_at": session.created_at.isoformat(),
            },
            status=201,
        )


@method_decorator(login_required, name="dispatch")
class ChatMessagesApiView(View):
    def get(self, request, session_id: int):
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        try:
            page_number = int(request.GET.get("page", "1") or 1)
        except ValueError:
            page_number = 1
        try:
            page_size = int(request.GET.get("page_size", str(settings.MESSAGE_PAGE_SIZE)) or settings.MESSAGE_PAGE_SIZE)
        except ValueError:
            page_size = settings.MESSAGE_PAGE_SIZE
        page_size = max(1, min(page_size, 100))

        messages_qs = session.messages.all().order_by("-timestamp")
        paginator = Paginator(messages_qs, page_size)
        page_obj = paginator.get_page(page_number)
        data = [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in reversed(list(page_obj.object_list))
        ]
        return JsonResponse(
            {
                "session_id": session.id,
                "messages": data,
                "pagination": {
                    "page": page_obj.number,
                    "page_size": page_size,
                    "total_pages": paginator.num_pages,
                    "has_next": page_obj.has_next(),
                    "has_previous": page_obj.has_previous(),
                },
            },
            status=200,
        )


@method_decorator(login_required, name="dispatch")
class ChatSendMessageApiView(View):
    def post(self, request, session_id: int):
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        if request.content_type and "application/json" in request.content_type:
            try:
                payload = json.loads(request.body.decode("utf-8")) if request.body else {}
            except json.JSONDecodeError:
                return JsonResponse({"detail": "Invalid JSON payload."}, status=400)
            content = (payload.get("content") or "").strip()
        else:
            content = request.POST.get("content", "").strip()

        if not content:
            return JsonResponse({"detail": "Message cannot be empty."}, status=400)
        if _free_tier_limit_reached(request.user):
            return JsonResponse({"detail": "Free daily message limit reached. Upgrade to Pro."}, status=403)

        user_msg = Message.objects.create(chat_session=session, role="user", content=content)
        latest_doc = Document.objects.filter(user=request.user).order_by("-uploaded_at").first()
        context_text = latest_doc.extracted_text if latest_doc else ""
        ai_service = AIService()
        reply = ai_service.generate_response(content, context=context_text)
        assistant_msg = Message.objects.create(chat_session=session, role="assistant", content=reply)
        return JsonResponse(
            {
                "session_id": session.id,
                "user_message": {
                    "id": user_msg.id,
                    "role": user_msg.role,
                    "content": user_msg.content,
                    "timestamp": user_msg.timestamp.isoformat(),
                },
                "assistant_message": {
                    "id": assistant_msg.id,
                    "role": assistant_msg.role,
                    "content": assistant_msg.content,
                    "timestamp": assistant_msg.timestamp.isoformat(),
                },
            },
            status=201,
        )
