from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import BasePermission

from .models import Message


class FreeTierMessageLimitPermission(BasePermission):
    message = "Free plan daily message limit reached. Upgrade to Pro for higher usage."

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.is_pro:
            return True
        if request.method != "POST":
            return True

        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        count = Message.objects.filter(
            chat_session__user=user,
            role="user",
            timestamp__gte=start_of_day,
        ).count()
        return count < settings.FREE_DAILY_MESSAGE_LIMIT
