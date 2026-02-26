from rest_framework import serializers

from .models import ChatSession, Message


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ("id", "title", "created_at")
        read_only_fields = ("id", "created_at")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "chat_session", "role", "content", "timestamp")
        read_only_fields = ("id", "timestamp")


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=4000)

    def validate_content(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Message content cannot be empty.")
        return cleaned
