from django.http import JsonResponse


class ProFeatureMiddleware:
    """
    Blocks Pro-only endpoints for free users.
    Voice endpoints are placeholders for future implementation.
    """

    PRO_ONLY_PREFIXES = ["/api/subscriptions/voice/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(prefix) for prefix in self.PRO_ONLY_PREFIXES):
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"detail": "Authentication required."}, status=401)
            if not user.is_pro:
                return JsonResponse({"detail": "Pro plan required for voice features."}, status=403)
        return self.get_response(request)
