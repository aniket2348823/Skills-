import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Checking for Image Generation models...")
found = False
try:
    for m in genai.list_models():
        if 'generateImages' in m.supported_generation_methods:
            print(f"FOUND IMAGE MODEL: {m.name}")
            found = True
except Exception as e:
    print(f"Error: {e}")

if not found:
    print("NO IMAGE GENERATION MODELS FOUND.")
