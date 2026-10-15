
import os
import json
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# App heading
st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and get AI-powered feedback "
    "for your target job role."
)

# Read API key from .env or Streamlit Cloud Secrets
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

# Resume upload and job role
uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

user_goal = st.text_input(
    "Target Job Role",
    placeholder="e.g. AI/ML Intern"
)

# Analyze button
if st.button("Analyze Resume", type="primary"):

    if not api_key:
        st.error(
            "Gemini API key not found. "
            "Check your .env file."
        )

    elif uploaded_file is None:
        st.warning("Please upload your resume PDF.")

    elif not user_goal.strip():
        st.warning("Please enter your target job role.")

    else:
        try:
            # Extract text from PDF
            reader = PdfReader(uploaded_file)

            resume_text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

            if not resume_text.strip():
                st.error(
                    "Could not extract text from this PDF. "
                    "Please upload a text-based PDF."
                )
                st.stop()

            # Create Gemini client
            client = genai.Client(api_key=api_key)

            # Prepare prompt
            prompt = f"""
You are a senior software engineer and hiring manager.

Analyze the resume for the target job role.

Target Job Role:
{user_goal}

Resume:
{resume_text}

Instructions:
1. Extract skills relevant to the target role.
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

            # Call Gemini with retries for temporary 503 errors
            with st.spinner("Analyzing your resume..."):

                response = None

                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt,
                            config={
                                "response_mime_type": "application/json"
                            }
                        )
                        break

                    except Exception as e:
                        error_message = str(e)

                        if "503" in error_message and attempt < 2:
                            time.sleep(5 * (attempt + 1))
                        else:
                            raise

            # Validate Gemini response
            if response is None or not response.text:
                st.error(
                    "Gemini returned an empty response. "
                    "Please try again."
                )
                st.stop()

            # Parse JSON response
            result = json.loads(response.text)

            if not isinstance(result, dict):
                raise ValueError("Gemini returned an unexpected response format.")

            # Display results
            st.success("Resume analysis completed!")

            st.subheader("✅ Relevant Skills")
            skills = result.get("skills", [])
            if skills:
                for item in skills:
                    st.markdown(f"- {item}")
            else:
                st.write("No skills returned.")

            st.subheader("📌 Missing Skills")
            missing_skills = result.get("missing_skills", [])
            if missing_skills:
                for item in missing_skills:
                    st.markdown(f"- {item}")
            else:
                st.write("No missing skills returned.")

            st.subheader("💡 Resume Improvement Suggestions")
            suggestions = result.get("suggestion", [])
            if suggestions:
                for item in suggestions:
                    st.markdown(f"- {item}")
            else:
                st.write("No suggestions returned.")

            st.subheader("🎯 Interview Questions")
            questions = result.get("interview_questions", [])
            if questions:
                for index, question in enumerate(questions, start=1):
                    st.markdown(f"{index}. {question}")
            else:
                st.write("No interview questions returned.")

        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.info(
                "If the error continues, check whether your Gemini "
                "API key, model access, and API quota are valid."
            )
