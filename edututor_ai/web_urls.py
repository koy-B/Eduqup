from django.urls import path

from accounts.web_views import DashboardView, HomeView, LoginPageView, LogoutPageView, PricingPageView, RegisterPageView
from chat.web_views import (
    ChatMessagesApiView,
    ChatSendMessageApiView,
    ChatSessionCreateApiView,
    ChatSessionCreatePageView,
    ChatSessionDetailView,
    ChatSessionListApiView,
)
from documents.web_views import DocumentUploadApiView, DocumentUploadPageView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("pricing/", PricingPageView.as_view(), name="pricing"),
    path("register/", RegisterPageView.as_view(), name="web-register"),
    path("login/", LoginPageView.as_view(), name="web-login"),
    path("logout/", LogoutPageView.as_view(), name="web-logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("chat/sessions/create/", ChatSessionCreatePageView.as_view(), name="web-chat-session-create"),
    path("chat/sessions/<int:session_id>/", ChatSessionDetailView.as_view(), name="web-chat-session-detail"),
    path("documents/upload/", DocumentUploadPageView.as_view(), name="web-document-upload"),
    path("app/api/chat/sessions/", ChatSessionListApiView.as_view(), name="web-api-chat-session-list"),
    path("app/api/chat/sessions/create/", ChatSessionCreateApiView.as_view(), name="web-api-chat-session-create"),
    path("app/api/chat/sessions/<int:session_id>/messages/", ChatMessagesApiView.as_view(), name="web-api-chat-messages"),
    path("app/api/chat/sessions/<int:session_id>/send/", ChatSendMessageApiView.as_view(), name="web-api-chat-send"),
    path("app/api/documents/upload/", DocumentUploadApiView.as_view(), name="web-api-doc-upload"),
]
