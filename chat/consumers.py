import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.utils import timezone

from ai_services.gemini_service import AIService
from documents.models import Document

from .models import ChatSession, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.session_id = int(self.scope["url_route"]["kwargs"]["session_id"])
        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return
        if not await self._user_owns_session(self.user.id, self.session_id):
            await self.close(code=4003)
            return

        self.group_name = f"chat_session_{self.session_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_json({"type": "error", "detail": "Invalid JSON payload."})
            return

        event_type = payload.get("type")
        if event_type == "typing":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "broadcast_typing",
                    "is_typing": bool(payload.get("is_typing", False)),
                    "user_id": self.user.id,
                },
            )
            return

        if event_type != "message":
            await self.send_json({"type": "error", "detail": "Unsupported event type."})
            return

        content = (payload.get("content") or "").strip()
        if not content:
            await self.send_json({"type": "error", "detail": "Message cannot be empty."})
            return

        if await self._free_tier_limit_reached(self.user.id):
            await self.send_json({"type": "error", "detail": "Free daily message limit reached. Upgrade to Pro."})
            return

        user_msg = await self._create_message("user", content)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_message",
                "message": user_msg,
            },
        )
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_typing",
                "is_typing": True,
                "user_id": 0,
            },
        )

        context_text = await self._latest_document_text(self.user.id)
        reply = await sync_to_async(AIService().generate_response)(content, context_text)
        assistant_msg = await self._create_message("assistant", reply)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_message",
                "message": assistant_msg,
            },
        )
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_typing",
                "is_typing": False,
                "user_id": 0,
            },
        )

    async def send_json(self, payload: dict):
        await self.send(text_data=json.dumps(payload))

    async def broadcast_message(self, event):
        await self.send_json({"type": "message", "message": event["message"]})

    async def broadcast_typing(self, event):
        await self.send_json(
            {
                "type": "typing",
                "is_typing": event["is_typing"],
                "user_id": event["user_id"],
            }
        )

    @database_sync_to_async
    def _user_owns_session(self, user_id: int, session_id: int) -> bool:
        return ChatSession.objects.filter(id=session_id, user_id=user_id).exists()

    @database_sync_to_async
    def _create_message(self, role: str, content: str) -> dict:
        msg = Message.objects.create(chat_session_id=self.session_id, role=role, content=content)
        return {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
        }

    @database_sync_to_async
    def _latest_document_text(self, user_id: int) -> str:
        doc = Document.objects.filter(user_id=user_id).order_by("-uploaded_at").first()
        return doc.extracted_text if doc else ""

    @database_sync_to_async
    def _free_tier_limit_reached(self, user_id: int) -> bool:
        user = self.user.__class__.objects.get(id=user_id)
        if user.is_pro:
            return False
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        count = Message.objects.filter(
            chat_session__user_id=user_id,
            role="user",
            timestamp__gte=start_of_day,
        ).count()
        return count >= settings.FREE_DAILY_MESSAGE_LIMIT
