from typing import Dict


DIFFICULTY_KEYWORDS = {
    2: {"summarize", "draft"},
    3: {"write", "create", "implement", "test", "run", "open"},
    4: {"build", "refactor"},
    5: {"deploy"},
}


def compute_difficulty(action_text: str) -> int:
    text = (action_text or "").lower()
    for level, words in DIFFICULTY_KEYWORDS.items():
        if any(w in text for w in words):
            return level
    return 3  # default medium difficulty


class MetricsCollector:
    def __init__(self) -> None:
        self.llm_total = 0
        self.llm_valid = 0
        self.rejections = 0
        self.actions_completed = 0
        self.cycles = 0
        self.score_sum = 0
        self.score_count = 0
        self.difficulty_sum = 0
        self.difficulty_count = 0

    def record_llm_response(self, valid: bool) -> None:
        self.llm_total += 1
        if valid:
            self.llm_valid += 1
        else:
            self.rejections += 1

    def record_evaluation(self, score: int, completed: bool, action_text: str) -> None:
        self.score_sum += score
        self.score_count += 1
        if completed:
            self.actions_completed += 1
        diff = compute_difficulty(action_text)
        self.difficulty_sum += diff
        self.difficulty_count += 1
        self.cycles += 1

    def snapshot(self) -> Dict[str, float]:
        llm_valid_rate = (self.llm_valid / self.llm_total) if self.llm_total else 0.0
        rejection_rate = (self.rejections / self.llm_total) if self.llm_total else 0.0
        action_completion_rate = (self.actions_completed / self.cycles) if self.cycles else 0.0
        user_usefulness_score_avg = (self.score_sum / self.score_count) if self.score_count else 0.0
        avg_task_difficulty_vs_completion = (self.difficulty_sum / self.difficulty_count) if self.difficulty_count else 0.0
        return {
            "llm_valid_output_rate": round(llm_valid_rate, 3),
            "action_completion_rate": round(action_completion_rate, 3),
            "user_usefulness_score_avg": round(user_usefulness_score_avg, 3),
            "rejection_rate": round(rejection_rate, 3),
            "avg_task_difficulty_vs_completion": round(avg_task_difficulty_vs_completion, 3),
        }
