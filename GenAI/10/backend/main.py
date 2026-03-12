from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import generate_image
from database import SessionLocal, ImageHistory
from schemas import GenerateRequest
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("generated", exist_ok=True)

@app.post("/generate")
def generate(data: GenerateRequest):
    image = generate_image(data.prompt, data.style)

    filename = f"{uuid.uuid4()}.png"
    path = f"generated/{filename}"

    image.save(path)

    db = SessionLocal()
    record = ImageHistory(
        prompt=data.prompt,
        style=data.style,
        image_path=path
    )
    db.add(record)
    db.commit()
    db.close()

    return {"image_url": path}

@app.get("/history")
def history():
    db = SessionLocal()
    records = db.query(ImageHistory).all()
    db.close()

    return records