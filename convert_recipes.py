import os
import re

TOML_PATH = r"C:\Users\Dell\.gemini\commands\gsd"
OUTPUT_PATH = r"C:\Users\Dell\.gemini\antigravity\scratch\Antigravity Skills\skills\recipes"

def convert_toml_to_md(filename):
    with open(os.path.join(TOML_PATH, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple extraction via regex (faster than adding toml dependency for one-off)
    desc_match = re.search(r'description\s*=\s*"(.*?)"', content, re.S)
    prompt_match = re.search(r'prompt\s*=\s*"(.*?)"', content, re.S)
    
    description = desc_match.group(1) if desc_match else "GSD Recipe"
    prompt = prompt_match.group(1) if prompt_match else ""
    
    # Unescape toml escape characters (\r\n, \", etc)
    prompt = prompt.replace('\\r', '').replace('\\n', '\n').replace('\\"', '"')
    
    md_content = f"# {filename.replace('.toml', '').replace('-', ' ').title()}\n\n"
    md_content += f"> [!NOTE]\n"
    md_content += f"> {description}\n\n"
    md_content += "## Recipe Logic\n"
    md_content += prompt + "\n"
    
    output_name = filename.replace('.toml', '.md')
    with open(os.path.join(OUTPUT_PATH, output_name), 'w', encoding='utf-8') as f:
        f.write(md_content)
    return output_name

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    
    count = 0
    for file in os.listdir(TOML_PATH):
        if file.endswith('.toml'):
            convert_toml_to_md(file)
            count += 1
    print(f"✅ Converted {count} GSD recipes to .md format.")
