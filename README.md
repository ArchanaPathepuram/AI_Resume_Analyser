from pathlib import Path

readme = r'''# AI Resume Analyser

An AI-powered resume analysis application built with **Python**, **Streamlit**, and the **Google Gemini API**. Upload a resume, select a target job role, and receive role-specific feedback to help identify relevant skills, missing skills, resume improvements, and interview preparation questions.

**Repository:** [ArchanaPathepuram/AI_Resume_Analyser](https://github.com/ArchanaPathepuram/AI_Resume_Analyser)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Configure the Gemini API Key](#configure-the-gemini-api-key)
- [Run the Application](#run-the-application)
- [Using the Application](#using-the-application)
- [Database](#database)
- [Security and Privacy](#security-and-privacy)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Author](#author)

## Overview

Reviewing a resume for a particular job can take time. This project uses Generative AI to analyse resume text in the context of a selected target role and return structured, actionable feedback.

The application extracts text from an uploaded PDF resume and sends the text, together with the target job role, to the Google Gemini model. The model returns a structured analysis containing relevant skills, missing skills, suggestions, and interview questions.

The project is intended as a resume-improvement and interview-preparation aid. Its feedback should be reviewed by the user and is not a guarantee of ATS results or hiring outcomes.

## Features

- **PDF Resume Upload:** Upload a resume in PDF format for analysis.
- **Role-Specific Analysis:** Provide a target job role so the feedback is relevant to the intended position.
- **Relevant Skills:** Identify skills in the resume that are relevant to the selected role.
- **Missing Skills:** Highlight potentially important skills that may not be demonstrated in the resume.
- **Resume Improvement Suggestions:** Receive practical recommendations for improving resume content.
- **Interview Question Generation:** Generate interview preparation questions based on the resume and target role.
- **Structured AI Output:** Request a predictable JSON response with separate sections for each analysis result.
- **Streamlit Interface:** Use a browser-based interface to interact with the application.
- **Environment-Based Configuration:** Load the Gemini API key from an environment variable or Streamlit secrets.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Google Gemini API | Generative AI-based resume analysis |
| Google Gen AI Python SDK (`google-genai`) | Communicates with the Gemini model |
| PyPDF | Extracts text from PDF resumes |
| `python-dotenv` | Loads environment variables from `.env` |
| JSON | Structures the AI-generated analysis |
| SQLite | Local database support in the repository |
| SQLAlchemy | Database engine and ORM models |

## How It Works

1. The user opens the Streamlit application.
2. The user uploads a PDF resume.
3. The application extracts text from the PDF using PyPDF.
4. The user provides a target job role.
5. The application sends the extracted resume text and target role to the Gemini model.
6. The model generates a structured response containing:
   - Relevant skills
   - Missing skills
   - Resume improvement suggestions
   - Interview questions
7. The application presents the results for the user to review.

### Workflow

```text
PDF Resume + Target Job Role
            |
            v
    PDF Text Extraction
            |
            v
   Resume Text + Role Prompt
            |
            v
      Google Gemini API
            |
            v
     Structured JSON Result
            |
            v
 Skills | Missing Skills | Suggestions | Interview Questions
```

## Project Structure

The repository currently contains the following main files:

```text
AI_Resume_Analyser/
├── .gitignore
├── ai.py                 # Gemini-powered resume analysis logic
├── app.py                # Application module
├── db.py                 # SQLite database connection and session setup
├── models.py             # SQLAlchemy database models
├── streamlit_app.py      # Streamlit user interface
└── README.md             # Project documentation
```

### Main Files

- **`streamlit_app.py`** — Streamlit interface, PDF upload flow, and user interaction.
- **`ai.py`** — Builds the role-specific prompt, calls the Gemini model, and parses the structured JSON response.
- **`app.py`** — Additional application logic included in the repository.
- **`db.py`** — Configures the SQLite database engine and SQLAlchemy session.
- **`models.py`** — Defines database models, including user and report records.
- **`.gitignore`** — Lists files and directories Git should ignore.

## Prerequisites

Install the following before running the project:

- Python **3.10 or later** (Python 3.11 is a suitable choice)
- Git
- A code editor such as Visual Studio Code
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

Check your Python and Git installations:

```bash
python --version
git --version
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ArchanaPathepuram/AI_Resume_Analyser.git
cd AI_Resume_Analyser
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the packages used by the application:

```bash
python -m pip install --upgrade pip
pip install streamlit google-genai python-dotenv pypdf sqlalchemy
```

If the repository includes a `requirements.txt` in a future update, you can install dependencies with:

```bash
pip install -r requirements.txt
```

## Configure the Gemini API Key

The application needs a valid Gemini API key to request AI-generated analysis.

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Create or obtain an API key, subject to Google's current availability and usage policies.
3. In the project's root directory, create a file named **`.env`**.
4. Add the following line:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your own key. Do not include quotation marks unless required by your environment setup.

The application uses the `GEMINI_API_KEY` environment variable and can also read Streamlit secrets where configured.

### Important API Key Safety

- Never commit your real `.env` file to GitHub.
- Never paste your API key into source code, screenshots, public issues, or README files.
- Ensure `.env` is listed in `.gitignore`.
- If a key is exposed, revoke or rotate it in Google AI Studio.
- API access, free quotas, model availability, and rate limits may change.

## Run the Application

From the repository root, with your virtual environment activated and `.env` configured, run:

```bash
streamlit run streamlit_app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser.

> If you are using a different entry-point file or have changed the project, check the corresponding run command in your current code.

## Using the Application

1. Start the application.
2. Upload your resume as a PDF.
3. Enter the job role you are targeting, such as **AI/ML Engineer**, **Data Analyst**, or **Software Developer**.
4. Start the analysis using the controls shown in the application.
5. Review the relevant skills identified in your resume.
6. Check the missing skills and decide which ones you genuinely have or need to learn.
7. Read the resume improvement suggestions and apply the changes that accurately reflect your experience.
8. Use the generated interview questions to prepare for the selected role.

**Tip:** Use a clear, text-based PDF resume for better text extraction. Scanned PDFs that contain only images may not produce usable text unless OCR is added.

## Database

The repository includes SQLite and SQLAlchemy support.

- **Database:** SQLite
- **Database file:** `resume_analyzer.db`
- **Database setup:** `db.py`
- **Database models:** `models.py`
- **User model:** Includes fields for email, password, verification status, and verification token.
- **Report model:** Includes fields for user association, resume text, and analysis result.

The database file is a local application data file. Do not publish real user records, credentials, or resume content in a public repository. For a fresh local setup, the application may create or initialize its database depending on how its startup code is configured.

## Security and Privacy

Resumes may contain personal and contact information. Use this application carefully:

- Only upload resumes you are authorised to process.
- Resume text submitted for AI analysis is sent to the configured Gemini service; review Google's applicable terms and privacy information before using sensitive documents.
- Keep API keys and other secrets out of source control.
- Avoid committing database files that contain personal data.
- For production use, passwords should be securely hashed, user authentication should be reviewed, and access controls should be tested.
- Delete uploaded or stored resume information when it is no longer needed, in accordance with your application's data-handling practices.

## Troubleshooting

### `GEMINI_API_KEY not found`

- Confirm that the file is named `.env`, not `.env.txt`.
- Put `.env` in the project root, where the application is launched.
- Check that the variable is named exactly `GEMINI_API_KEY`.
- Restart Streamlit after changing environment configuration.

### Gemini API errors or rate limits

- Verify that the API key is valid and that the selected model is available to your account.
- Check current quota, billing, and rate-limit information in Google AI Studio.
- Retry later if the service is temporarily overloaded.
- Do not assume that a model name or free quota will remain available indefinitely.

### PDF text is empty or incomplete

- Try a text-based PDF instead of a scanned image.
- Check that the PDF is not password-protected or corrupted.
- OCR support may be needed for scanned documents.

### `ModuleNotFoundError`

Activate the project's virtual environment and install the missing package. For example:

```bash
pip install streamlit google-genai python-dotenv pypdf sqlalchemy
```

### Port 8501 is already in use

Run Streamlit on another port:

```bash
streamlit run streamlit_app.py --server.port 8502
```

Then open `http://localhost:8502`.

## Future Improvements

Possible enhancements include:

- Add a `requirements.txt` for reproducible installation.
- Add automated tests for PDF extraction and AI response handling.
- Add input validation and clearer error messages for malformed PDFs and API failures.
- Support additional document formats where appropriate.
- Add optional job-description matching and keyword comparison.
- Add downloadable analysis reports.
- Improve authentication, password hashing, and data-retention controls before production deployment.
- Add screenshots or a demo link after deployment.

## Author

**Archana Pathepuram**

- GitHub: [@ArchanaPathepuram](https://github.com/ArchanaPathepuram)
- Project Repository: [AI_Resume_Analyser](https://github.com/ArchanaPathepuram/AI_Resume_Analyser)

---

If this project helps you, consider giving the repository a ⭐ on GitHub.
'''
path = Path("/mnt/data/README_AI_Resume_Analyser.md")
path.write_text(readme, encoding="utf-8")
print(f"Created: {path}")
