from openai import OpenAI
from openai.types.shared.reasoning import Reasoning

from config import OPENAI_API_KEY
from schemas import AngularComponentSpec

client = OpenAI(api_key=OPENAI_API_KEY)

INSTRUCTIONS = """
You are an expert Angular UI Engineer and Visual Layout Interpreter.
Your job is to transform a UI mockup image into a fully functional Angular Standalone Component...
"""

def generate_component(input_text: str, base64_image: str):

    user_input = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": input_text},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

    response = client.responses.parse(
        instructions=INSTRUCTIONS,
        model="gpt-5.2",
        reasoning=Reasoning(effort="low", summary="auto"),
        text_format=AngularComponentSpec,
        input=user_input
    )

    return response.output_parsed.dict()