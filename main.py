from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from docx import Document
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import io
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Groq setup
# -----------------------------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-20b"


# -----------------------------
# Pydantic response structure
# -----------------------------

class ResumeResult(BaseModel):
    skills_match: int
    experience_match: int
    projects_match: int
    education_match: int

    skills_found: list[str]
    skills_missing: list[str]

    summary: str


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Resume Ranker API is running!"
    }


# -----------------------------
# Extract resume text
# -----------------------------

def extract_text(file_bytes, filename):

    # PDF
    if filename.lower().endswith(".pdf"):

        pdf = PdfReader(io.BytesIO(file_bytes))

        text = ""

        for page in pdf.pages:
            text += page.extract_text() or ""

        return text

    # DOCX
    elif filename.lower().endswith(".docx"):

        document = Document(io.BytesIO(file_bytes))

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        raise ValueError("Only PDF and DOCX files are supported")


# -----------------------------
# Analyze Resume
# -----------------------------

@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    hr_requirements: str = Form(...)
):

    # Read uploaded file
    file_bytes = await file.read()

    # Extract resume text
    resume_text = extract_text(
        file_bytes,
        file.filename
    )

    # Prompt for Groq
    prompt = f"""
You are an HR resume screening assistant.

Compare the candidate's resume against the HR requirements.

HR Requirements:
{hr_requirements}

Candidate Resume:
{resume_text}

Analyze the candidate in these four categories:

1. skills_match
2. experience_match
3. projects_match
4. education_match

Give each category a score from 0 to 100.

Return ONLY valid JSON:

{{
    "skills_match": 0,
    "experience_match": 0,
    "projects_match": 0,
    "education_match": 0,
    "skills_found": [],
    "skills_missing": [],
    "summary": ""
}}

Rules:

- Each score must be between 0 and 100.
- skills_found = required skills that appear in the resume.
- skills_missing = required skills that are not found.
- Do not invent experience.
- Do not invent skills.
- summary should briefly explain the candidate's suitability.
"""

    # Call Groq
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    answer = response.choices[0].message.content

    # Convert JSON string → Python dictionary
    data = json.loads(answer)

    # Validate using Pydantic
    result = ResumeResult(**data)
    final_score = (
    result.skills_match * 0.40
    + result.experience_match * 0.25
    + result.projects_match * 0.20
    + result.education_match * 0.15
    )
    return {
    "match_percentage": round(final_score),
    "skills_match": result.skills_match,
    "experience_match": result.experience_match,
    "projects_match": result.projects_match,
    "education_match": result.education_match,
    "skills_found": result.skills_found,
    "skills_missing": result.skills_missing,
    "summary": result.summary
    }
    