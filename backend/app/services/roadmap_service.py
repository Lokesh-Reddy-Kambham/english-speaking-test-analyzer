WEAK_AREA_TASKS = {
    "grammar": [
        "Revise tense consistency and subject-verb agreement.",
        "Rewrite five spoken answers into cleaner sentence structures.",
        "Record a one-minute answer and correct grammar errors from the transcript.",
    ],
    "fluency": [
        "Do three one-minute no-pause speaking drills.",
        "Practice chunking ideas into short phrases before recording.",
        "Repeat the same answer twice and reduce filler words on the second attempt.",
    ],
    "vocabulary": [
        "Learn ten role-specific words and use them in sample answers.",
        "Replace repeated words with stronger alternatives.",
        "Summarize an article using professional vocabulary.",
    ],
    "communication": [
        "Use a beginning, middle, and closing sentence for every answer.",
        "Practice concise examples with situation, action, and result.",
        "Ask for clarification and confirm next steps in role-play answers.",
    ],
    "confidence": [
        "Record daily answers while maintaining steady volume.",
        "Practice with a timer and finish with a clear closing sentence.",
        "Listen to your recording and mark moments where energy drops.",
    ],
}


def build_roadmap(scores: dict, mode: str, weeks: int = 12) -> list[dict]:
    weeks = weeks if weeks in {4, 8, 12} else 12
    ranked_weak_areas = sorted(
        ["grammar", "fluency", "vocabulary", "communication", "confidence"],
        key=lambda key: scores[key],
    )
    primary = ranked_weak_areas[:3]
    roadmap = []

    for week in range(1, weeks + 1):
        area = primary[(week - 1) % len(primary)]
        tasks = WEAK_AREA_TASKS[area]
        mode_task = (
            "Add one technical interview-style answer using concise architecture or implementation language."
            if mode == "IT"
            else "Add one customer conversation answer focused on clarity, empathy, and resolution."
        )
        roadmap.append(
            {
                "week": week,
                "focus": area.title(),
                "title": f"Week {week}: strengthen {area}",
                "tasks": [tasks[(week - 1) % len(tasks)], mode_task, "Take one speaking test and compare scores."],
                "target_score": min(10, round(scores[area] + 0.3 * week, 1)),
            }
        )
    return roadmap
