import torch
from diffusers import StableDiffusionPipeline
from config import DEVICE, SD_MODEL, HF_TOKEN_ENV, OUTPUT_DIR
import os

class ImageGenerator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            SD_MODEL,
            local_files_only=True,
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
        ).to(DEVICE)

        self.pipe.safety_checker = None
        self.save_dir = os.path.join(OUTPUT_DIR, "images")
        os.makedirs(self.save_dir, exist_ok=True)

    def generate_images(self, captions, guidance_scale=6.5, steps=25):
        images = []
        for i, caption in enumerate(captions):
            generator = torch.Generator(device=DEVICE).manual_seed(42 + i)
            result = self.pipe(
                caption,
                guidance_scale=guidance_scale,
                height=512,
                width=512,
                num_inference_steps=steps,
                generator=generator
            )

            img = result.images[0]
            file_path = os.path.join(self.save_dir, f"panel_{i+1:02d}.png")
            img.save(file_path)

            print(f"[Saved] {file_path}")

            images.append((caption, img))

        return images
