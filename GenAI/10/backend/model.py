import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = "segmind/tiny-sd"
device = "cuda" if torch.cuda.is_available() else "cpu"


def get_pipeline():
    global pipe
    if pipe is None:
        print("Loading model...")
        if device == "cuda":
            pipe = StableDiffusionPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=torch.float16
            )
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=torch.float32
            )

        pipe = pipe.to(device)
        print("Model loaded.")

    return pipe


def generate_image(prompt: str, style: str):
    pipe = get_pipeline()

    full_prompt = f"{prompt}, {style}, ultra detailed"
    image = pipe(full_prompt, num_inference_steps=20).images[0]

    return image