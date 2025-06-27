def load_skill_list(filepath='data/skills_list.txt'):
    with open(filepath, 'r') as file:
        skills = [line.strip().lower() for line in file if line.strip()]
    return skills

def match_skills(resume_text, skill_list):
    matched = [skill for skill in skill_list if skill in resume_text]
    missing = list(set(skill_list) - set(matched))
    return matched, missing

def calculate_score(matched, total):
    return round((len(matched) / total) * 100, 2) if total > 0 else 0
