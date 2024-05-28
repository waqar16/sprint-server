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
    cultural_and_seasonal: str = Field(description="the cultural and seasonal of the picture")
    technical_aspects: str = Field(description="Technology and the technical aspects of the picture")


parser = JsonOutputParser(pydantic_object=ImageInformation)


def process_image_data(image_base64: str):
    vision_prompt = """
    Given the image, provide the following information:
    - The design style is hand drawn and visual style is filled and complexity is detailed.
    - A picture belongs to which category or theme, for example image related to Eid day, Christmas, Independence Day.
    - Purpose of the picture for example is decorative, intended for use in holiday greeting cards.
    - Content of the picture for example the image contains a detailed, hand-drawn picture.
    - The cultural and seasonal of the picture.
    - A picture related to which technology aspects.
    """

    @chain                                                  # chain decorator to make it runnable
    def image_model(inputs: dict):
        model = ChatOpenAI(temperature=0.5, model="gpt-4-vision-preview", max_tokens=1024)
        msg = model.invoke(
            [HumanMessage(
                content=[
                    {"type": "text", "text": inputs["prompt"]},
                    {"type": "text", "text": parser.get_format_instructions()},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
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
