import requests
import time
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = [
    "qwen2.5-coder:0.5b",
    "qwen3.5:0.8b"
]

PROMPT = "Explain the difference between a reflected XSS and a stored XSS in one sentence. Then provide a simple payload for each."

def test_model(model_name):
    print(f"\n--- Testing Model: {model_name} ---")
    payload = {
        "model": model_name,
        "prompt": PROMPT,
        "stream": False
    }
    
    start_time = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            latency = end_time - start_time
            content = data.get("response", "")
            
            print(f"Status: ONLINE")
            print(f"Ping (Latency): {latency:.2f}s")
            print(f"Content Quality (Preview):\n{content[:500]}...")
            return {
                "model": model_name,
                "status": "ONLINE",
                "latency": latency,
                "content": content
            }
        else:
            print(f"Status: FAILED (HTTP {response.status_code})")
            return {"model": model_name, "status": "FAILED"}
            
    except Exception as e:
        print(f"Status: ERROR ({str(e)})")
        return {"model": model_name, "status": "ERROR"}

if __name__ == "__main__":
    results = []
    for model in MODELS:
        results.append(test_model(model))
    
    with open("llm_results.json", "w") as f:
        json.dump(results, f, indent=4)
