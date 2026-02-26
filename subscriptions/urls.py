from django.urls import path

from .views import (
    SpeechToTextPlaceholderView,
    SubscriptionStatusView,
    TextToSpeechPlaceholderView,
)

urlpatterns = [
    path("status/", SubscriptionStatusView.as_view(), name="subscription-status"),
    path("voice/speech-to-text/", SpeechToTextPlaceholderView.as_view(), name="speech-to-text"),
    path("voice/text-to-speech/", TextToSpeechPlaceholderView.as_view(), name="text-to-speech"),
]
