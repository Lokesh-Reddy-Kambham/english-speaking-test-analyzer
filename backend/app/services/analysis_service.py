import re
from collections import Counter
from functools import lru_cache

from app.config import get_settings

settings = get_settings()

FILLER_WORDS = {"um", "uh", "like", "basically", "actually", "you know", "i mean", "sort of", "kind of"}
PROFESSIONAL_WORDS = {
    "coordinate", "collaborate", "prioritize", "deliver", "analyze", "stakeholder", "timeline",
    "requirement", "solution", "impact", "customer", "process", "strategy", "implementation",
    "architecture", "debug", "deploy", "scalable", "secure", "optimize", "document", "clarify",
}
IT_TERMS = {"api", "database", "server", "frontend", "backend", "cloud", "deployment", "algorithm", "system", "testing"}
NON_IT_TERMS = {"customer", "service", "support", "explain", "resolve", "clarity", "conversation", "relationship"}


@lru_cache
def _language_tool():
    try:
        import language_tool_python
    except ImportError as exc:
        raise RuntimeError("language-tool-python is not installed. Install backend requirements and Java for grammar analysis.") from exc
    return language_tool_python.LanguageTool(settings.languagetool_language)


def _words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def _sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[.!?]+", text) if item.strip()]


def analyze_transcript(text: str, audio_metrics: dict, mode: str) -> dict:
    words = _words(text)
    word_count = len(words)
    unique_words = set(words)
    sentences = _sentences(text)
    duration_minutes = max(audio_metrics["duration_seconds"] / 60, 0.01)
    wpm = round(word_count / duration_minutes, 1)

    matches = _language_tool().check(text) if text else []
    grammar_issue_count = len([m for m in matches if m.ruleIssueType in {"grammar", "misspelling", "typographical"}])
    filler_counts = _count_fillers(text)
    total_fillers = sum(filler_counts.values())
    repeated = {word: count for word, count in Counter(words).items() if count >= 3 and word not in {"the", "and", "to", "a", "i"}}
    repeated_ratio = round(sum(repeated.values()) / max(word_count, 1), 2)
    vocabulary_diversity = round(len(unique_words) / max(word_count, 1), 2)
    avg_sentence_length = round(word_count / max(len(sentences), 1), 1)
    professional_hits = sorted((unique_words & PROFESSIONAL_WORDS) | (unique_words & (IT_TERMS if mode == "IT" else NON_IT_TERMS)))

    grammar_score = _clamp(10 - grammar_issue_count * 0.7 - max(0, avg_sentence_length - 24) * 0.08)
    fluency_score = _score_fluency(wpm, total_fillers, audio_metrics)
    vocabulary_score = _clamp(4 + vocabulary_diversity * 6 + min(len(professional_hits), 8) * 0.25 - repeated_ratio * 3)
    communication_score = _score_communication(mode, professional_hits, avg_sentence_length, word_count)
    confidence_score = _clamp(5 + audio_metrics["voice_energy"] * 3 - audio_metrics["average_pause_duration"] * 0.7 - total_fillers * 0.12)
    overall = round((grammar_score + fluency_score + vocabulary_score + communication_score + confidence_score) / 5, 1)

    metrics = {
        "word_count": word_count,
        "unique_word_count": len(unique_words),
        "vocabulary_diversity": vocabulary_diversity,
        "repeated_word_ratio": repeated_ratio,
        "repeated_words": repeated,
        "sentence_count": len(sentences),
        "average_sentence_length": avg_sentence_length,
        "words_per_minute": wpm,
        "filler_words": filler_counts,
        "grammar_issue_count": grammar_issue_count,
        "grammar_issues": [{"message": m.message, "context": m.context, "offset": m.offset} for m in matches[:20]],
        "professional_vocabulary": professional_hits,
        **audio_metrics,
    }

    scores = {
        "grammar": grammar_score,
        "fluency": fluency_score,
        "vocabulary": vocabulary_score,
        "communication": communication_score,
        "confidence": confidence_score,
        "overall": overall,
        "metrics": metrics,
    }
    return {"scores": scores, "feedback": generate_feedback(scores, mode)}


def _count_fillers(text: str) -> dict[str, int]:
    lowered = text.lower()
    counts = {}
    for filler in FILLER_WORDS:
        pattern = r"\b" + re.escape(filler) + r"\b"
        count = len(re.findall(pattern, lowered))
        if count:
            counts[filler] = count
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def _score_fluency(wpm: float, fillers: int, audio_metrics: dict) -> float:
    if 110 <= wpm <= 155:
        speed_score = 10
    elif 90 <= wpm < 110 or 155 < wpm <= 175:
        speed_score = 8
    else:
        speed_score = 6
    return _clamp(speed_score - fillers * 0.2 - audio_metrics["average_pause_duration"] * 0.8 - audio_metrics["pause_count"] * 0.05)


def _score_communication(mode: str, professional_hits: list[str], avg_sentence_length: float, word_count: int) -> float:
    baseline = 6.5 if word_count >= 60 else 5.5
    concise_bonus = 1 if 8 <= avg_sentence_length <= 22 else -0.8
    domain_bonus = min(len(professional_hits), 6) * (0.35 if mode == "IT" else 0.3)
    return _clamp(baseline + concise_bonus + domain_bonus)


def generate_feedback(scores: dict, mode: str) -> dict:
    strengths = []
    improvements = []
    metrics = scores["metrics"]

    if scores["grammar"] >= 8:
        strengths.append("Your grammar is mostly accurate and easy to follow.")
    else:
        improvements.append("Improve sentence structure and review the grammar issues highlighted in the transcript.")

    if scores["fluency"] >= 8:
        strengths.append("Your pace and continuity sound natural.")
    else:
        improvements.append("Reduce filler words and practice speaking continuously for one to two minutes.")

    if scores["vocabulary"] >= 8:
        strengths.append("You used a varied and professional vocabulary.")
    else:
        improvements.append("Increase vocabulary variety and replace repeated words with precise alternatives.")

    if scores["communication"] < 7:
        if mode == "IT":
            improvements.append("Practice concise technical explanations using problem, approach, result, and impact.")
        else:
            improvements.append("Practice clear customer-friendly explanations with empathy and simple next steps.")
    else:
        strengths.append("Your message is organized for the selected communication mode.")

    if metrics["filler_words"]:
        improvements.append(f"Your most common fillers were: {', '.join(metrics['filler_words'].keys())}.")
    if not strengths:
        strengths.append("You completed the speaking sample and provided enough material for a focused improvement plan.")

    return {"strengths": strengths, "improvements": improvements}


def _clamp(value: float) -> float:
    return round(max(0, min(10, value)), 1)
