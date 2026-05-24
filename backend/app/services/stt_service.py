from functools import lru_cache

from app.config import get_settings

settings = get_settings()


@lru_cache
def _load_model():
    try:
        import whisper
    except ImportError as exc:
        raise RuntimeError("openai-whisper is not installed. Install it with Python 3.11 or 3.12 for local transcription.") from exc
    return whisper.load_model(settings.whisper_model)


def transcribe_audio(audio_path: str) -> dict:
    model = _load_model()
    result = model.transcribe(audio_path, fp16=False)
    return {
        "text": result.get("text", "").strip(),
        "language": result.get("language", "en"),
        "segments": result.get("segments", []),
    }
