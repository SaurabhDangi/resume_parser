#  AI Resume Ranker

An AI-powered resume screening and ranking system that compares multiple candidate resumes against HR requirements and ranks candidates based on their suitability.

The system supports PDF and DOCX resumes, uses Groq LLM for resume analysis, validates AI responses with Pydantic, and provides a deployed FastAPI backend with a web frontend.

---

## 🚀 Live Demo

### Frontend
https://resume-parser-eight-sigma.vercel.app

### Backend API
https://resume-parser-nod7.onrender.com

### API Documentation
https://resume-parser-nod7.onrender.com/docs

---

## ✨ Features

- 📄 Upload multiple resumes at once
- 📑 Supports PDF and DOCX files
- 🤖 AI-powered resume analysis using Groq
- 🧠 Compares resumes against HR requirements
- 📊 Calculates candidate match percentage
- 🏆 Automatically ranks candidates
- 🔍 Identifies skills found and missing
- 📈 Separate scores for:
  - Skills
  - Experience
  - Projects
  - Education
- 📝 Generates an AI-based candidate summary
- ⚡ FastAPI REST API
- 🌐 Deployed backend using Render
- 💻 Deployed frontend using Vercel

---

## 🏗️ Architecture

```text
                    USER
                     │
                     ▼
          ┌─────────────────────┐
          │      Frontend       │
          │    HTML / CSS / JS  │
          │      Vercel         │
          └──────────┬──────────┘
                     │
                     │ HTTP POST
                     ▼
          ┌─────────────────────┐
          │      FastAPI        │
          │      Backend        │
          │      Render         │
          └──────────┬──────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    PDF / DOCX Parser        Groq LLM
       pypdf                 AI Analysis
     python-docx                  │
          │                       │
          └──────────┬────────────┘
                     ▼
                Pydantic
              Validation
                     │
                     ▼
             Weighted Scoring
                     │
                     ▼
              Candidate Ranking
                     │
                     ▼
                  JSON
                     │
                     ▼
                Frontend
