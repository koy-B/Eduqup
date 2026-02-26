from django.conf import settings
from rest_framework import serializers

from .models import Document

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "file", "extracted_text", "uploaded_at")
        read_only_fields = ("id", "extracted_text", "uploaded_at")

    def validate_file(self, value):
        filename = value.name.lower()
        ext = "." + filename.split(".")[-1] if "." in filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError("Unsupported file type. Allowed: pdf, docx, jpg, jpeg, png.")

        max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(f"File too large. Max allowed is {settings.MAX_UPLOAD_SIZE_MB}MB.")
        return value
