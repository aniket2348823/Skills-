import json
import os

INDEX_PATH = r"C:\Users\Dell\.gemini\antigravity\scratch\Antigravity Skills\skills\skills_index.json"
RECIPES_DIR = r"C:\Users\Dell\.gemini\antigravity\scratch\Antigravity Skills\skills\recipes"

def update_index():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    for file in os.listdir(RECIPES_DIR):
        if file.endswith('.md'):
            # Key format: recipe-[file-slug]
            key = f"recipe-{file.replace('.md', '').lower()}"
            index[key] = f"skills/recipes/{file}"
    
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    print(f"✅ Registered {len(os.listdir(RECIPES_DIR))} recipes in skills_index.json.")

if __name__ == "__main__":
    update_index()
