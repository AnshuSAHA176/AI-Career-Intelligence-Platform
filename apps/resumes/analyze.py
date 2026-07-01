import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

ROLE_SKILLS = {
    "backend developer": [
        "python",
        "django",
        "sql",
        "postgresql",
        "docker",
        "git",
        "aws",
    ],
    "data scientist": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "sql",
    ],
    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git",
    ],
}


def analyze_resume(text, target_role):
    skills = ROLE_SKILLS.get(target_role.lower(), [])

    if not skills:
        return {
            "score": 0,
            "found_skills": [],
            "missing_skills": [],
        }

    text = text.lower()

    found = [skill for skill in skills if skill in text]
    missing = [skill for skill in skills if skill not in text]

    score = int((len(found) / len(skills)) * 100)

    return {
        "score": score,
        "found_skills": found,
        "missing_skills": missing,
    }


SYSTEM_PROMPT = """
You are an expert technical recruiter, ATS evaluator and hiring manager.

Analyze ONE resume for ONE target role.

Return ONLY valid JSON.

Rules:

- No markdown.
- No explanation.
- No ```json
- Score must be 0-100.
- Do not hallucinate skills.
- Every field is required.
- secondary_roles must be a JSON array.
- technologies must be a JSON array.
- experience must be an object.
- Return valid JSON parsable by json.loads().

Return EXACTLY this schema:

{
    "score": 0,
    "found_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "summary": "",
    "primary_role": "",
    "secondary_roles": [],
    "technologies": [],
    "experience": {
        "years": null
    }
}
"""


def analyze_resume_ai(text, target_role):

    user_prompt = f"""
Target Role:
{target_role}

Resume:

{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0,
        max_tokens=1500,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    print(content)

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"AI returned invalid JSON:\n{content}")

    return {
        "score": data.get("score", 0),
        "found_skills": data.get("found_skills", []),
        "missing_skills": data.get("missing_skills", []),
        "strengths": data.get("strengths", []),
        "weaknesses": data.get("weaknesses", []),
        "suggestions": data.get("suggestions", []),
        "summary": data.get("summary", ""),
        "primary_role": data.get("primary_role", ""),
        "secondary_roles": data.get("secondary_roles", []),
        "technologies": data.get("technologies", []),
        "experience": data.get("experience", {}),
    }