import base64
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from langchain_openai import ChatOpenAI
from app.utils import process_image_data

OPENAI_API_KEY = settings.OPENAI_API_KEY
ICON_FINDER_KEY = settings.ICON_FINDER_KEY
fast_llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", streaming=True)


class ImageProcessView(APIView):

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        result = process_image_data(image_base64)

        style = result.get("style", "")
        category = result.get("category", "")
        context = result.get("context", "")
        content_specifics = result.get("content_specifics", "")
        technical_aspects = result.get("technical_aspects", "")
        query = f"{style} {category} {context} {content_specifics} {technical_aspects}"
        # query = 'Arrow'
        url = f"https://api.iconfinder.com/v4/icons/search?query={query}&count=5"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {ICON_FINDER_KEY}"
        }

        response = requests.get(url, headers=headers)
        json_data = response.json()

        icon_data_list = []
        for icon in json_data['icons']:
            for raster_size in icon['raster_sizes']:
                for format_info in raster_size['formats']:
                    icon_data = {
                        'preview_url': format_info['preview_url'],
                        'download_url': format_info['download_url']
                    }
                    icon_data_list.append(icon_data)
        print(icon_data_list)
        print(len(icon_data_list))
        return Response(icon_data_list, status=status.HTTP_200_OK)
