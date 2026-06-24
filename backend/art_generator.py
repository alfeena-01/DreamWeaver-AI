from diffusers import StableDiffusionPipeline
import torch
import os
from datetime import datetime
from PIL import Image, ImageDraw

# Local Stable Diffusion model loading, no external API keys required.
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

print(f"[INFO] Loading Stable Diffusion model on {device} with dtype={torch_dtype}...")
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch_dtype,
    local_files_only=True
).to(device)
print("[INFO] Model loaded successfully.")

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def fast_fallback(prompt):
    img = Image.new('RGB', (512, 512), color='lightblue')
    d = ImageDraw.Draw(img)
    d.text((10,10), f"Dream: {prompt}", fill=(0,0,0))
    return img

def generate_art(prompt: str, save: bool = False):
    """
    Generate an image from a dream description using Stable Diffusion Turbo.
    Automatically adjusts steps for GPU vs CPU.
    """
    try:
        if torch.cuda.is_available():
            steps = 8
            print(f">>> Generating art with {steps} steps on GPU")
            image = pipe(prompt, num_inference_steps=steps).images[0]
        else:
            print("[INFO] Using fast fallback mode (CPU)")
            image = fast_fallback(prompt)

        if save:
            filename = f"dream_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(ARTIFACTS_DIR, filename)
            image.save(filepath)
            print(f"[INFO] Dream visual saved at {filepath}")

        print(">>> Image generation finished")
        return image
    except Exception as e:
        print(f"[ERROR] Art generation failed: {e}")
        return None
