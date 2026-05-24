from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import get_settings

settings = get_settings()


def save_upload(file: UploadFile) -> str:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "speech.webm").suffix or ".webm"
    target = upload_dir / f"{uuid4().hex}{suffix}"
    with target.open("wb") as buffer:
        buffer.write(file.file.read())
    return str(target)


def get_audio_metrics(audio_path: str) -> dict:
    try:
        import librosa
        import numpy as np
        from pydub import AudioSegment, silence
    except ImportError as exc:
        raise RuntimeError("librosa, numpy, and pydub are required for audio metrics. Install backend requirements in a compatible Python environment.") from exc

    audio = AudioSegment.from_file(audio_path)
    duration_seconds = max(len(audio) / 1000, 0.1)
    silent_ranges = silence.detect_silence(audio, min_silence_len=450, silence_thresh=audio.dBFS - 14)
    pauses = [(end - start) / 1000 for start, end in silent_ranges]

    y, sr = librosa.load(audio_path, sr=None, mono=True)
    rms = librosa.feature.rms(y=y)[0] if len(y) else np.array([0])
    confidence_energy = float(np.clip(np.mean(rms) * 35, 0, 1))

    return {
        "duration_seconds": round(duration_seconds, 2),
        "pause_count": len(pauses),
        "average_pause_duration": round(float(np.mean(pauses)) if pauses else 0, 2),
        "total_pause_duration": round(float(np.sum(pauses)) if pauses else 0, 2),
        "voice_energy": round(confidence_energy, 2),
    }
