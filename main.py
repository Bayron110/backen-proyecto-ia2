from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
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
    file: UploadFile = File(...),
    instruction: str = Form(...)
):

    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    result = generate_component(
        instruction,
        base64_image
    )

    return result