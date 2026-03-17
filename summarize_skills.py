import json
import os
from collections import defaultdict

def summarize_skills():
    index_path = r"D:\antigravity-awesome-skills\skills_index.json"
    output_path = r"C:\Users\Dell\.gemini\antigravity\brain\7e2458b3-7453-4543-89da-528deb3c30a4\skills_overview.md"
    
    with open(index_path, 'r', encoding='utf-8') as f:
        skills = json.load(f)
        
    categories = defaultdict(list)
    for skill in skills:
        cat = skill.get("category", "Uncategorized")
        if not cat:
            cat = "Uncategorized"
        categories[cat].append(skill)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Integrated Skills Overview\n\n")
        f.write(f"There are **{len(skills)}** skills integrated into the IDE. Due to the large number of skills, they have been grouped into **{len(categories)}** categories.\n\n")
        
        # Sort categories by number of skills, descending
        sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
        
        for cat, cat_skills in sorted_categories:
            f.write(f"## {cat.title()} ({len(cat_skills)} skills)\n")
            # Sample up to 5 skills per category
            samples = cat_skills[:5]
            for skill in samples:
                name = skill.get('name', skill.get('id', 'Unnamed'))
                desc = skill.get('description', '')
                if len(desc) > 150:
                    desc = desc[:147] + "..."
                f.write(f"- **{name}**: {desc}\n")
            if len(cat_skills) > 5:
                f.write(f"- *...and {len(cat_skills) - 5} more*\n")
            f.write("\n")

if __name__ == "__main__":
    summarize_skills()
