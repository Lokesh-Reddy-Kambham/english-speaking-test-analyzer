from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ScoreResponse(BaseModel):
    grammar: float
    fluency: float
    vocabulary: float
    communication: float
    confidence: float
    overall: float
    metrics: dict[str, Any]


class FeedbackResponse(BaseModel):
    strengths: list[str]
    improvements: list[str]
    roadmap: list[dict[str, Any]]


class TestResponse(BaseModel):
    id: int
    mode: str
    prompt: str | None
    duration_seconds: float
    transcript: str
    scores: ScoreResponse
    feedback: FeedbackResponse
    created_at: datetime


class RoadmapUpdateRequest(BaseModel):
    completed: bool
    notes: str | None = Field(default=None, max_length=1000)
