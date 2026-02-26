from django.conf import settings
from django.db import models


class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to="documents/")
    extracted_text = models.TextField(blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Document {self.id} - user {self.user_id}"
