from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
from services.openai_service import generate_component


app = FastAPI()

# Permitir conexión desde Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción cambia esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(
    file: UploadFile = File(...),
    instruction: str = Form(...)
):

    # Leer imagen
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # 🔥 AQUÍ VA ESTO
    result = generate_component(
        instruction,
        base64_image
    )

    return result