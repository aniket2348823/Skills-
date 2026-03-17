from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
import os
from dotenv import load_dotenv
from .services.gemini import analyze_and_title
from .services.imagen import enhance_image

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Product Enhancer Agent API is running"})

@app.post("/api/process")
async def process_image(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read file bytes for AI services
        with open(temp_filename, "rb") as f:
            image_bytes = f.read()

        # 1. Analyze with Gemini
        gemini_result = await analyze_and_title(image_bytes)
        if not gemini_result:
             raise HTTPException(status_code=500, detail="Failed to analyze image with Gemini")
        
        title = gemini_result.get("title")
        prompt = gemini_result.get("prompt")

        # 2. Enhance with Gemini Imagen
        enhanced_image_b64 = await enhance_image(image_bytes, prompt)
        if not enhanced_image_b64:
             raise HTTPException(status_code=500, detail="Failed to generate image with Gemini Imagen")

        # Clean up temp file
        os.remove(temp_filename)

        return {
            "title": title,
            "prompt_used": prompt,
            "enhanced_image": enhanced_image_b64 
        }

    except Exception as e:
        if os.path.exists(f"temp_{file.filename}"):
            os.remove(f"temp_{file.filename}")
        raise HTTPException(status_code=500, detail=str(e))
