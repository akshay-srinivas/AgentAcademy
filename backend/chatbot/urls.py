from django.urls import path
from . import views

urlpatterns = [
    path(
        "chatbot/",
        views.stream_ai_chatbot_response,
        name="ai-chatbot-streaming",
    ),
]