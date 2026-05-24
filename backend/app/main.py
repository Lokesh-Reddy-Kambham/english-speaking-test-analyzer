from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, engine
from app import models
from app.routes import dashboard, roadmap, tests

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(tests.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name}
