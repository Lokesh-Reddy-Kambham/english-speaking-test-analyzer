from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.test import RoadmapProgress
from app.schemas.test import RoadmapUpdateRequest

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


@router.get("/progress")
def list_progress(db: Session = Depends(get_db)):
    rows = (
        db.query(RoadmapProgress)
        .order_by(RoadmapProgress.week_number.asc(), RoadmapProgress.id.asc())
        .all()
    )
    return [
        {
            "id": row.id,
            "test_id": row.test_id,
            "week_number": row.week_number,
            "title": row.title,
            "completed": row.completed,
            "notes": row.notes,
        }
        for row in rows
    ]


@router.patch("/progress/{progress_id}")
def update_progress(
    progress_id: int,
    payload: RoadmapUpdateRequest,
    db: Session = Depends(get_db),
):
    row = (
        db.query(RoadmapProgress)
        .filter(RoadmapProgress.id == progress_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Roadmap item not found")
    row.completed = payload.completed
    row.notes = payload.notes
    db.commit()
    return {"message": "Progress updated"}
