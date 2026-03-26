from openai import OpenAI
from openai.types.shared.reasoning import Reasoning
from typing import Optional, List, Dict, Any

from config import OPENAI_API_KEY
from schemas import AngularComponentSpec

client = OpenAI(api_key=OPENAI_API_KEY)

INSTRUCTIONS = """
You are an expert Angular UI Engineer and Visual Layout Interpreter.
Your job is to transform a UI mockup image into a fully functional Angular Standalone Component.

If the user provides conversation context, use it to maintain continuity.
If the user does not provide an image, generate the component only from the text instruction and context.
Return only valid structured output.
"""

def generate_component(
    instruction: str,
    base64_image: Optional[str] = None,
    context: Optional[List[Dict[str, Any]]] = None
):
    if context is None:
        context = []

    context_text = ""
    if context:
        context_text = "\n\nConversation context:\n"
        for msg in context[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            context_text += f"{role}: {content}\n"

    full_text = f"{instruction}{context_text}"

    content = [
        {"type": "input_text", "text": full_text}
    ]

    if base64_image:
        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{base64_image}"
        })

    user_input = [
        {
            "role": "user",
            "content": content
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