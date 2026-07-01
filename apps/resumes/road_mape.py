ROADMAPS = {
    "django": [
        "Learn Django Models",
        "Learn Django Views",
        "Build CRUD API"
    ],

    "postgresql": [
        "Learn SQL Basics",
        "Learn JOINs",
        "Connect PostgreSQL with Django"
    ],

    "docker": [
        "Learn Docker Images",
        "Learn Docker Containers",
        "Dockerize Django Project"
    ]
}

JOB_SKILLS = {
    "backend developer": [
        "python",
        "django",
        "sql",
        "postgresql",
        "docker",
        "git",
        "aws",
        "rest api"
    ],

    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git",
        "redux",
        "typescript"
    ],

    "full stack developer": [
        "html",
        "css",
        "javascript",
        "react",
        "python",
        "django",
        "postgresql",
        "docker",
        "git"
    ],

    "data scientist": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "sql",
        "statistics",
        "matplotlib"
    ]
}
def road_map(missing_skill):
    roadmap=[{
            "skill": skill,
            "steps": ROADMAPS.get(skill, [])
        } for skill in missing_skill ]
    
    return roadmap

def match_resume(required_skills,found_skill):
    
    matched_skills=[skill for skill in found_skill if skill in required_skills]
    missing_skills = [skill for skill in required_skills if skill not in matched_skills]
    
    score = round(
    len(matched_skills)
    / len(required_skills)
    * 100
)
   
    return {
    "match_score": score,
    "matched_skills": matched_skills,
    'missing_skills':missing_skills

    
}

def level_cheaker(score):
    if score>70:
        return "Strong Match"
    elif score >= 40:
        return "Moderate Match"

    else:
        return "Weak Match"