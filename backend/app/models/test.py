from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SpeakingTest(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mode: Mapped[str] = mapped_column(String(20), nullable=False)
    prompt: Mapped[str | None] = mapped_column(Text)
    audio_path: Mapped[str] = mapped_column(String(500), nullable=False)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    transcript = relationship("Transcript", back_populates="test", uselist=False, cascade="all, delete-orphan")
    score = relationship("Score", back_populates="test", uselist=False, cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="test", uselist=False, cascade="all, delete-orphan")


class Transcript(Base):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), unique=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(20), default="en")
    segments: Mapped[list | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    test = relationship("SpeakingTest", back_populates="transcript")


class Score(Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), unique=True, nullable=False)
    grammar: Mapped[float] = mapped_column(Float, nullable=False)
    fluency: Mapped[float] = mapped_column(Float, nullable=False)
    vocabulary: Mapped[float] = mapped_column(Float, nullable=False)
    communication: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    overall: Mapped[float] = mapped_column(Float, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    test = relationship("SpeakingTest", back_populates="score")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), unique=True, nullable=False)
    strengths: Mapped[list] = mapped_column(JSON, nullable=False)
    improvements: Mapped[list] = mapped_column(JSON, nullable=False)
    roadmap: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    test = relationship("SpeakingTest", back_populates="feedback")


class RoadmapProgress(Base):
    __tablename__ = "roadmap_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int | None] = mapped_column(ForeignKey("tests.id"))
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    notes: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
