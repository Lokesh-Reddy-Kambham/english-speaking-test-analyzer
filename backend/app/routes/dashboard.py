from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.test import RoadmapProgress, SpeakingTest

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    tests = (
        db.query(SpeakingTest)
        .order_by(SpeakingTest.created_at.asc())
        .all()
    )
    progress = db.query(RoadmapProgress).all()
    chart_data = [
        {
            "date": test.created_at.strftime("%Y-%m-%d"),
            "overall": test.score.overall,
            "grammar": test.score.grammar,
            "fluency": test.score.fluency,
            "vocabulary": test.score.vocabulary,
            "communication": test.score.communication,
            "confidence": test.score.confidence,
        }
        for test in tests
        if test.score
    ]
    latest = chart_data[-1] if chart_data else None
    completed = len([item for item in progress if item.completed])
    return {
        "total_tests": len(chart_data),
        "latest_scores": latest,
        "score_history": chart_data,
        "roadmap": {
            "total": len(progress),
            "completed": completed,
            "completion_rate": round(completed / max(len(progress), 1) * 100, 1),
        },
        "streak": _estimate_streak(tests),
    }


def _estimate_streak(tests: list[SpeakingTest]) -> int:
    unique_days = {test.created_at.date() for test in tests}
    return len(unique_days)
