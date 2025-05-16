
import json
from chatbot.actions.chatbot_agent import ChatBotAgent
from django.http import (
    JsonResponse,
    StreamingHttpResponse,
)
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@csrf_exempt
def stream_ai_chatbot_response(request):

    request_data = json.loads(request.body)

    copilot_action = ChatBotAgent()

    print("Request data:", request_data)
        
    return StreamingHttpResponse(
        copilot_action.execute(
            user_query=request_data["user_query"],
        ),
        status=status.HTTP_200_OK,
    )