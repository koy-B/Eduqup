from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SubscriptionStatusView(APIView):
    def get(self, request):
        user = request.user
        return Response(
            {
                "is_pro": user.is_pro,
                "subscription_start": user.subscription_start,
                "subscription_end": user.subscription_end,
            },
            status=status.HTTP_200_OK,
        )


class SpeechToTextPlaceholderView(APIView):
    def post(self, request):
        # Future: integrate streaming/audio transcription provider for Pro users.
        return Response(
            {"detail": "Voice speech-to-text is planned and not implemented yet."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class TextToSpeechPlaceholderView(APIView):
    def post(self, request):
        # Future: integrate voice synthesis provider for Pro users.
        return Response(
            {"detail": "Voice text-to-speech is planned and not implemented yet."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
