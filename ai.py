from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def analyze_resume(resume_text, user_goal):

    prompt = f"""
You are a senior software engineer and hiring manager.

Analyze the resume for the target job role.

Target Job Role:
{user_goal}

Resume:
{resume_text}

Instructions:
1. Extract only skills relevant to the target role.
2. Identify important missing skills.
3. Give practical resume improvement suggestions.
4. Generate interview questions based on the resume and role.
5. Make the analysis specific to the selected job role.

Return only valid JSON in this exact format:
{{
    "skills": [],
    "missing_skills": [],
    "suggestion": [],
    "interview_questions": []
}}

All four fields must contain lists of strings.
Do not include Markdown or code fences.
"""

    try:
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Check your .env file."
            )

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "skills": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        },
                        "missing_skills": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        },
                        "suggestion": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        },
                        "interview_questions": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        }
                    },
                    "required": [
                        "skills",
                        "missing_skills",
                        "suggestion",
                        "interview_questions"
                    ]
                }
            }
        )

        content = response.text

        if not content:
            raise ValueError("Gemini returned an empty response.")

        return json.loads(content)

    except Exception as e:
        return {
            "error": str(e),
            "skills": [],
            "missing_skills": [],
            "suggestion": [],
            "interview_questions": []
        }
