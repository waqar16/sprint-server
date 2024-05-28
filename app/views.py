import base64
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from langchain_openai import ChatOpenAI

from app.utils import process_image_data

OPENAI_API_KEY = settings.OPENAI_API_KEY
fast_llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", streaming=True)


class ImageProcessView(APIView):

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        result = process_image_data(image_base64)
        return Response(result, status=status.HTTP_200_OK)
