from django.urls import path

from .views import ChatSessionCreateView, ChatSessionListView, SendMessageView

urlpatterns = [
    path("sessions/", ChatSessionListView.as_view(), name="chat-session-list"),
    path("sessions/create/", ChatSessionCreateView.as_view(), name="chat-session-create"),
    path("sessions/<int:session_id>/messages/", SendMessageView.as_view(), name="send-message"),
]
