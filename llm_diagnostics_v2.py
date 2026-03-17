import requests
import time
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

# Testing multiple models to narrow down the bottleneck
MODELS = [
    "qwen2.5:0.5b",
    "qwen2.5-coder:0.5b",
    "qwen3.5:0.8b"
]

def test_pings():
    results = {}
    for model in MODELS:
        print(f"\n[PING] Model: {model}")
        start = time.time()
        try:
            # Simple "hi" to check responsiveness and cold-start
            resp = requests.post(OLLAMA_URL, json={
                "model": model, "prompt": "hi", "stream": False
            }, timeout=150) # Extended timeout for 0.8b
            latency = time.time() - start
            if resp.status_code == 200:
                print(f" -> ONLINE | Latency: {latency:.2f}s")
                results[model] = {"status": "ONLINE", "ping": latency}
            else:
                print(f" -> ERROR {resp.status_code}")
                results[model] = {"status": "HTTP_ERROR", "code": resp.status_code}
        except Exception as e:
            print(f" -> TIMEOUT/ERROR: {str(e)}")
            results[model] = {"status": "TIMEOUT"}
    return results

def test_quality(model):
    print(f"\n[QUALITY] Testing {model} logic...")
    prompt = "Write a Python function to check if a string is a palindrome. Output only the code."
    start = time.time()
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": model, "prompt": prompt, "stream": False
        }, timeout=150)
        latency = time.time() - start
        if resp.status_code == 200:
            content = resp.json().get("response", "")
            print(f" -> QUALITY OK | Latency: {latency:.2f}s")
            return {"status": "OK", "latency": latency, "content": content}
    except:
        return {"status": "FAIL"}

if __name__ == "__main__":
    pings = test_pings()
    # Test quality only on the 3.5 if it survives the ping
    if pings.get("qwen3.5:0.8b", {}).get("status") == "ONLINE":
        quality_35 = test_quality("qwen3.5:0.8b")
    else:
        quality_35 = "N/A"
        
    final_report = {
        "pings": pings,
        "quality_3_5": quality_35
    }
    with open("llm_final_audit.json", "w") as f:
        json.dump(final_report, f, indent=4)
