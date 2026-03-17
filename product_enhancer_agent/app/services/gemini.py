import os
import google.generativeai as genai
import json

async def analyze_and_title(image_bytes):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found.")
        return None

    genai.configure(api_key=api_key)
    
    # Use a model that supports vision, e.g., gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = """
    Analyze this product image. 
    1. Generate a catchy, short, high-converting e-commerce title for this product.
    2. Describe a perfect, professional, high-end studio setting for this product. This description will be used as a prompt for an image generator to create a new background. Be specific about lighting (e.g., soft box, rim light), background texture (e.g., marble, wood, solid pastel), and composition. Keep the prompt under 70 words.
    
    Return the result as a JSON object with keys: "title" and "prompt".
    Do not include Markdown formatting (```json ... ```) in the response, just the raw JSON string.
    """

    try:
        # Gemini expects image parts in a specific format
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': image_bytes}, 
            prompt
        ])
        
        text_response = response.text.strip()
        # Clean up potential markdown code blocks if Gemini adds them
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        return json.loads(text_response)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None
