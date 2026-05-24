from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.test import Feedback, RoadmapProgress, Score, SpeakingTest, Transcript
from app.schemas.test import TestResponse
from app.services.analysis_service import analyze_transcript
from app.services.audio_service import get_audio_metrics, save_upload
from app.services.roadmap_service import build_roadmap
from app.services.stt_service import transcribe_audio

router = APIRouter(prefix="/tests", tags=["Speaking Tests"])


@router.post("/analyze", response_model=TestResponse)
def analyze_test(
    mode: str = Form(default="IT"),
    roadmap_weeks: int = Form(default=12),
    prompt: str | None = Form(default=None),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if mode not in {"IT", "Non-IT"}:
        raise HTTPException(status_code=422, detail="Mode must be IT or Non-IT")

    try:
        audio_path = save_upload(audio)
        audio_metrics = get_audio_metrics(audio_path)
        transcript_result = transcribe_audio(audio_path)
        analysis = analyze_transcript(transcript_result["text"], audio_metrics, mode)
        roadmap = build_roadmap(analysis["scores"], mode, roadmap_weeks)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {exc}") from exc

    test = SpeakingTest(
        mode=mode,
        prompt=prompt,
        audio_path=audio_path,
        duration_seconds=audio_metrics["duration_seconds"],
    )
    db.add(test)
    db.flush()

    transcript = Transcript(
        test_id=test.id,
        text=transcript_result["text"],
        language=transcript_result["language"],
        segments=transcript_result["segments"],
    )
    scores = analysis["scores"]
    score = Score(test_id=test.id, **scores)
    feedback = Feedback(
        test_id=test.id,
        strengths=analysis["feedback"]["strengths"],
        improvements=analysis["feedback"]["improvements"],
        roadmap=roadmap,
    )
    db.add_all([transcript, score, feedback])
    for item in roadmap:
        db.add(RoadmapProgress(test_id=test.id, week_number=item["week"], title=item["title"]))
    db.commit()
    db.refresh(test)
    return _serialize_test(test)


@router.get("", response_model=list[TestResponse])
def list_tests(db: Session = Depends(get_db)):
    tests = (
        db.query(SpeakingTest)
        .order_by(SpeakingTest.created_at.desc())
        .limit(25)
        .all()
    )
    return [_serialize_test(test) for test in tests if test.transcript and test.score and test.feedback]


@router.get("/{test_id}", response_model=TestResponse)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(SpeakingTest).filter(SpeakingTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return _serialize_test(test)


def _serialize_test(test: SpeakingTest) -> dict:
    return {
        "id": test.id,
        "mode": test.mode,
        "prompt": test.prompt,
        "duration_seconds": test.duration_seconds,
        "transcript": test.transcript.text,
        "scores": {
            "grammar": test.score.grammar,
            "fluency": test.score.fluency,
            "vocabulary": test.score.vocabulary,
            "communication": test.score.communication,
            "confidence": test.score.confidence,
            "overall": test.score.overall,
            "metrics": test.score.metrics,
        },
        "feedback": {
            "strengths": test.feedback.strengths,
            "improvements": test.feedback.improvements,
            "roadmap": test.feedback.roadmap,
        },
        "created_at": test.created_at,
    }
