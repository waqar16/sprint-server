import base64
import os


from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel


OPENAI_API_KEY = settings.OPENAI_API_KEY
fast_llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", streaming=True)


class UploadImageView(APIView):

    def post(self, request, *args, **kwargs):
        image = request.data.get('image')

        if not image:
            return Response({'error': 'image is required'}, status=status.HTTP_400_BAD_REQUEST)
        file_name, extension = os.path.splitext(image.name)

        if extension in ['.png']:

            image_content = image.read()
            image_data = base64.b64encode(image_content).decode('utf-8')

            class OUTPUT(BaseModel):
                style: str
                context: str
                content: str

            outline_parser = PydanticOutputParser(pydantic_object=OUTPUT)

            prompt_template = """
                You are Image AI assistant, your have to provide some useful information related to given image.
                - Give Provide image Style like flat or drawn, Category or Theme like Business, technology.
                - Give me Context and usage purpose like Web, mobile kids, adults, healthcare etc.
                - Give me Content specifies for example animal, food, cooking sports and cultural seasonal like Ramadan,
                 Chinese New year, Independence Day.
                 
                Follow Instruction: {format_instructions}
            """

            PROMPT = PromptTemplate(template=prompt_template,  input_variables=["url"],
                                    partial_variables={
                                        "format_instructions": outline_parser.get_format_instructions()
                                    })

            step1_answer_chain = PROMPT | fast_llm | outline_parser
            answer = step1_answer_chain.invoke({'url': f"data:image/jpeg;base64,{image_data}"})
            return Response(data=answer, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'PNG images only'}, status=status.HTTP_400_BAD_REQUEST)

        # headers = {
        #     "Authorization": f"Bearer {OPENAI_API_KEY}",
        #     "Content-Type": "application/json"
        # }
        #
        # payload = {
        #     "model": "gpt-4-vision-preview",
        #     "messages": [
        #         {
        #             "role": "user",
        #             "content": [
        #                 {
        #                     "type": "text",
        #                     "text": "What’s in this image?"
        #                 },
        #                 {
        #                     "type": "image_url",
        #                     "image_url": {
        #                         "url": f"data:image/jpeg;base64,{image_data}"
        #                     }
        #                 }
        #             ]
        #         }
        #     ],
        #     "max_tokens": 500
        # }

        # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        # print(response.json())


 # 1.Style:
                #     Design Style (e.g., Flat, Hand drawn)
                #     Visual Style (e.g., Outline, Filled)
                #     Complexity (e.g., Simple, Detailed)
                # 2. Category/Theme:
                #     General Theme (e.g., Business, Technology)
                #     Specific Theme (e.g., Holidays, Sports)
                #     Industry (e.g., Healthcare, Education)
                # 3. Context/Usage:
                #     Usage Context (e.g., Web, Mobile)
                #     Audience (e.g., Kids, Adults)
                #     Purpose (e.g., Decorative, Informative)
                # 4. Content Specifics:
                #     Objects (e.g., Animals, Food)
                #     Activities (e.g., Cooking, Sports)
                #     Concepts (e.g., Abstract, Love & Romance)
                # 5. Cultural and Seasonal:
                #     Cultural Events (e.g., Chinese New Year, Ramadan)
