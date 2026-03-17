import asyncio
import aiohttp
import json

async def check_embedding():
    url = "http://localhost:11434/api/embeddings"
    model = "qwen3.5:0.8b"
    print(f"Testing embeddings for {model}...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={
                "model": model,
                "prompt": "The quick brown fox jumps over the lazy dog"
            }) as resp:
                print(f"Status: {resp.status}")
                text = await resp.text()
                print(f"Response: {text[:200]}...")
                if resp.status == 200:
                    data = json.loads(text)
                    if "embedding" in data:
                        print("SUCCESS: Embedding generated.")
                    else:
                        print("FAILURE: Embedding key missing.")
                else:
                    print(f"FAILURE: HTTP {resp.status}")
    except Exception as e:
        print(f"ERROR: {e}")

async def check_audit_quality():
    import sys
    sys.path.insert(0, r"D:\Antigravity 2\API Endpoint Scanner")
    from backend.ai.cortex import CortexEngine
    cortex = CortexEngine()
    # Test with 0.8b model
    cortex.OLLAMA_MODEL = "qwen3.5:0.8b"
    print(f"\nTesting Audit Reasoning with {cortex.OLLAMA_MODEL}...")
    vuln_data = {
        "type": "IDOR",
        "url": "/api/v1/users/2/secrets",
        "description": "CRITICAL VULNERABILITY: Changing user ID from 1 to 2 allowed access to private secret data of another user. Response confirms data leak.",
        "baseline_response": '{"email": "user1@test.com", "secret": "abc"}',
        "response_entropy": 95,
        "force_mode": "DEEP_MODE"
    }
    res = await cortex.audit_candidate(vuln_data)
    print(f"Audit Result: {json.dumps(res, indent=2)}")

if __name__ == "__main__":
    asyncio.run(check_embedding())
    asyncio.run(check_audit_quality())
