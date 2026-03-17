import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.getcwd(), 'Antigravity Skills'))

from core.skill_router import SkillRouter

def test_gsd_resolution():
    router = SkillRouter()
    
    test_queries = [
        "research how to implement a phase",
        "execute a project roadmap",
        "verify the progress of work",
        "debug a system crash",
        "plan a new milestone"
    ]
    
    print("--- TESTING GSD RECIPE RESOLUTION ---")
    for query in test_queries:
        result = router.route_query(query)
        print(f"Query: '{query}' -> Resolved to: {result}")
    print("--- RESOLUTION TEST COMPLETE ---")

if __name__ == "__main__":
    test_gsd_resolution()
