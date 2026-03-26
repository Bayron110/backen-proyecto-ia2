from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import base64
import json

from services.openai_service import generate_component

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(
    instruction: str = Form(""),
    context: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    base64_image = None
    conversation_context = []

    # Si viene contexto, lo convertimos de texto JSON a lista
    if context:
        try:
            conversation_context = json.loads(context)
        except Exception:
            conversation_context = []

    # Si viene imagen, la procesamos
    if file is not None:
        image_bytes = await file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

    result = generate_component(
        instruction=instruction,
        base64_image=base64_image,
        context=conversation_context
    )

    return result