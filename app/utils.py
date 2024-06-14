from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from langchain_core.output_parsers import JsonOutputParser


class ImageInformation(BaseModel):
    style: str = Field(description="the shape of the picture")
    category: str = Field(description="the category of the picture belongs to")
    context: str = Field(description="The purpose of the picture")
    content_specifics: str = Field(description="Content of the image related")
    cultural_and_seasonal: str = Field(
        description="the cultural and seasonal of the picture")
    technical_aspects: str = Field(
        description="Technology and the technical aspects of the picture")


parser = JsonOutputParser(pydantic_object=ImageInformation)


def process_image_data(image_base64: str):
    vision_prompt = """
    Given the image, provide the following information:
    
    Identify and List Image Attributes

Please review the uploaded image and identify any attributes from the list below that are present. Extract and list these attributes accordingly:

Style

Design Style: e.g., Flat, Handdrawn
Visual Style: e.g., Outline, Filled
Complexity: e.g., Simple, Detailed
Category/Theme

General Theme: e.g., Business, Technology
Specific Theme: e.g., Holidays, Sports
Industry: e.g., Healthcare, Education
Context/Usage

Usage Context: e.g., Web, Mobile
Audience: e.g., Kids, Adults
Purpose: e.g., Decorative, Informative
Content Specifics

Objects: e.g., Animals, Food
Activities: e.g., Cooking, Sports
Concepts: e.g., Abstract, Love & Romance
Cultural and Seasonal

Cultural Events: e.g., Chinese New Year, Ramadan
Seasons: e.g., Summer, Winter
Holidays: e.g., Christmas, Easter
Technical Aspects

Technology: e.g., AI, Mobile Devices
Health & Fitness: e.g., Yoga, Gym
    """

    # chain decorator to make it runnable
    @chain
    def image_model(inputs: dict):
        model = ChatOpenAI(
            temperature=0.5, model="gpt-4-vision-preview", max_tokens=1024)
        msg = model.invoke(
            [HumanMessage(
                content=[
                    {"type": "text", "text": inputs["prompt"]},
                    {"type": "text", "text": parser.get_format_instructions()},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{inputs['image']}"}},
                ])]
        )
        return msg.content

    load_image_chain = TransformChain(
        input_variables=["image"],
        output_variables=["image"],
        transform=lambda x: {"image": image_base64}
    )

    vision_chain = load_image_chain | image_model | parser
    return vision_chain.invoke({'image': image_base64, 'prompt': vision_prompt})
