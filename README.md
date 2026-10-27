# AI Resume Analyser

AI Resume Analyser is a Python project that helps users review their resumes for a particular job role. It uses the Google Gemini API to analyse the resume and provide suggestions for improvement.

## About the Project

I built this project to make resume checking easier. Users can upload their resume in PDF format and enter the job role they are interested in. The application analyses the resume and provides feedback that can help them prepare for job applications and interviews.

## Features

- Upload a resume in PDF format.
- Enter the job role you want to apply for.
- Extract text from the uploaded resume.
- Identify relevant skills and skills that may be missing.
- Get suggestions to improve the resume.
- Generate interview questions based on the selected role.
- View the analysis through a Streamlit interface.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google Gen AI SDK
- PyPDF
- SQLite
- SQLAlchemy
- Python-dotenv

## How It Works

1. Upload your resume as a PDF file.
2. Enter your target job role, such as AI/ML Engineer or Data Analyst.
3. The application extracts the text from your resume.
4. The resume content and job role are sent to the Gemini model for analysis.
5. The application displays the generated feedback, including skills, improvement suggestions, and interview questions.

## Project Structure

```text
AI_Resume_Analyser/
├── ai.py
├── app.py
├── db.py
├── models.py
├── streamlit_app.py
├── .gitignore
└── README.md
```

- `streamlit_app.py` – Provides the user interface.
- `ai.py` – Handles AI-based resume analysis.
- `app.py` – Contains additional application logic.
- `db.py` – Handles database configuration.
- `models.py` – Defines the database models.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ArchanaPathepuram/AI_Resume_Analyser.git
cd AI_Resume_Analyser
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

For Windows:

```bash
.venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install streamlit google-genai python-dotenv pypdf sqlalchemy
```

### 4. Set up the API key

Create a file named `.env` in the project folder and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace the example value with your own API key from [Google AI Studio](https://aistudio.google.com/).

Do not upload your actual API key to GitHub.

### 5. Run the application

```bash
streamlit run streamlit_app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Database

The project includes SQLite and SQLAlchemy for database operations. The database models support storing user information and resume analysis reports, depending on the application flow.

## Future Improvements

- Add job description matching.
- Support additional resume formats.
- Allow users to download analysis reports.
- Improve error handling and input validation.
- Add more options for resume analysis.

## Author

**Archana Pathepuram**

GitHub: [ArchanaPathepuram](https://github.com/ArchanaPathepuram)

Project: [AI Resume Analyser](https://github.com/ArchanaPathepuram/AI_Resume_Analyser)
