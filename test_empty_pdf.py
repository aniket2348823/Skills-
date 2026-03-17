import asyncio
import os
import sys

sys.path.append(os.path.abspath(r'd:\Antigravity 2\API Endpoint Scanner'))
from backend.core.reporting import ReportGenerator

async def test_empty():
    rg = ReportGenerator()
    telemetry = {
        "start_time": "2024-03-05 10:00:00",
        "end_time": "2024-03-05 10:01:00",
        "duration": "60",
        "total_requests": 1500,
        "avg_latency_ms": 35,
        "peak_concurrency": 10,
        "ai_calls": 0,
        "llm_avg_latency": 0,
        "circuit_breaker_activations": 0
    }
    await rg.generate_report("EMPTY_TEST", [], "http://example.com", telemetry)
    print("Empty report generated.")

asyncio.run(test_empty())
