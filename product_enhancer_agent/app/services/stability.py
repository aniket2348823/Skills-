import os
import requests
import base64

async def enhance_image(image_bytes, prompt):
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        print("Error: STABILITY_API_KEY not found.")
        return None

    # Using Stable Image Core or SDXL for image-to-image/in-painting/background generation
    # For "enhancing" and "background", typically we might use 'stable-diffusion-xl-1024-v1-img2img' 
    # or a specific background replacement endpoint if available. 
    # Let's use SDXL img2img for general enhancement with a high strength (meaning more change allowed) 
    # or lower strength to preserve structure.
    # Actually, for "product background", Stability has a specific tool 'stable-image-edit-replace-background' 
    # but that might be more complex. Let's stick to SDXL img2img for now as a general "enhancer" 
    # or use the 'structure' control if we want to be fancy.
    
    # Let's try the standard SDXL img2img endpoint first.
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-img2img"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    body = {
        "steps": 40,
        "cfg_scale": 7,
        "init_image_mode": "IMAGE_STRENGTH",
        "image_strength": 0.25, # Low strength = mostly original image. We want to change background so maybe higher? 
                                # Actually, standard img2img changes the WHOLE image. 
                                # If we want to keep the product EXACTLY the same, we need masking or background replacement.
                                # For this MVP, let's try a balanced strength (0.35) to "enhance" it without destroying it,
                                # combined with a strong prompt.
        "samples": 1,
        "text_prompts": [
            {"text": prompt, "weight": 1},
            {"text": "blurry, low quality, distorted, ugly, bad anatomy", "weight": -1}
        ],
    }
    
    # We need to pass the file. The requests library handles multipart for files usually, 
    # but Stability API for img2img expects 'init_image' as a file part.
    
    files = {
        "init_image": image_bytes
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=body)
        
        if response.status_code != 200:
            print(f"Stability API Error: {response.status_code} - {response.text}")
            return None

        data = response.json()
        # Stability returns base64 images
        return data["artifacts"][0]["base64"]

    except Exception as e:
        print(f"Stability Service Exception: {e}")
        return None
