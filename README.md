# English Speaking Test Analyzer

A lightweight MVP for analyzing English speaking ability without paid AI APIs or user accounts. Users open the app, record or upload speech, get a transcript, view rule-based scores, receive feedback, and generate a personalized roadmap.

## Live Demo

Frontend: https://frontend-seven-gules-39.vercel.app

Note: analysis endpoints require the backend to be running or deployed and configured with `VITE_API_URL`.

## Render Deployment

This repo includes a `render.yaml` Blueprint for deploying the FastAPI backend and a Render Postgres database.

1. Open https://dashboard.render.com/blueprints.
2. Create a new Blueprint from this GitHub repository.
3. Render will create `speak-meter-backend` and `speak-meter-db`.
4. After the backend deploys, copy its `https://...onrender.com` URL.
5. In Vercel, set `VITE_API_URL` to `https://your-render-backend.onrender.com/api` and redeploy the frontend.

## What It Does

- Records speech in the browser or accepts an uploaded audio file.
- Converts speech to text using local open-source Whisper.
- Checks grammar and spelling with LanguageTool.
- Uses librosa and pydub for audio metrics such as duration, pauses, and voice energy.
- Scores grammar, fluency, vocabulary, communication, confidence, and overall proficiency.
- Detects filler words such as `um`, `uh`, `like`, `basically`, and `actually`.
- Supports IT and Non-IT communication modes.
- Generates 4, 8, or 12 week rule-based improvement roadmaps.
- Shows dashboard history, progress charts, roadmap progress, and downloadable reports.

No login, register, JWT, sessions, user roles, email verification, forgot password, OAuth, or social login are included.

## Project Structure

```text
backend/
  app/
    models/       SQLAlchemy models for tests, transcripts, scores, feedback
    routes/       FastAPI routes for analysis, dashboard, roadmap
    schemas/      Pydantic response/request models
    services/     Whisper, audio, analysis, and roadmap logic
  uploads/        Local audio storage
  requirements.txt
frontend/
  src/
    components/   Recorder, charts, score cards, report views
    pages/        Speaking test and dashboard
    services/     API client
database/
  schema.sql      PostgreSQL schema
```

## Backend Setup

Install system dependencies:

- PostgreSQL
- FFmpeg
- Java, required by LanguageTool
- Python 3.11 or 3.12 recommended for Whisper and audio packages

From `backend/`:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

From `frontend/`:

```powershell
npm install
copy .env.example .env
npm.cmd run dev -- --host 127.0.0.1
```

Frontend:

```text
http://127.0.0.1:5173
```

## API Structure

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/tests/analyze` | Upload recorded audio and generate transcript, scores, feedback, roadmap |
| `GET` | `/api/tests` | List recent anonymous speaking tests |
| `GET` | `/api/tests/{test_id}` | View a single test report |
| `GET` | `/api/dashboard/analytics` | Score history, roadmap summary, streak estimate |
| `GET` | `/api/roadmap/progress` | List generated roadmap progress items |
| `PATCH` | `/api/roadmap/progress/{progress_id}` | Mark a roadmap item complete or open |

## Scoring Logic

- Grammar score decreases with LanguageTool grammar, spelling, and typographical issues.
- Fluency score uses words per minute, pause count, pause duration, and filler words.
- Vocabulary score uses unique-word ratio, repeated-word ratio, and professional vocabulary hits.
- Communication score rewards concise, structured communication for IT or Non-IT mode.
- Confidence score uses voice energy, pauses, and filler frequency.

The analysis is rule-based and local. No ChatGPT, Gemini, Claude, hosted AI APIs, or paid AI services are used.
