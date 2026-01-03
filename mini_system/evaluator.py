from typing import Dict, Any, Optional

CONCRETE_VERBS = {
    "write",
    "create",
    "run",
    "open",
    "implement",
    "test",
    "build",
    "deploy",
    "refactor",
    "draft",
    "summarize",
    "break",
}

VAGUE_TERMS = {
    "think",
    "consider",
    "explore",
    "research",
    "brainstorm",
    "ponder",
    "maybe",
}


def evaluate(proposal: Dict[str, str], user_feedback: Optional[int] = None) -> Dict[str, Any]:
    """Return binary validity and scalar usefulness score (1–5).

    Heuristic:
    - Penalize overly vague actions.
    - Reward presence of concrete verbs and actionable phrasing.
    - Optionally combine with user feedback (1–5) via simple average.
    """
    action = (proposal.get("action") or "").lower()
    reason = (proposal.get("reason") or "").lower()

    # Base score
    score = 3

    # Vagueness penalty
    if any(term in action for term in VAGUE_TERMS):
        score -= 1

    # Concrete boost
    if any(verb in action for verb in CONCRETE_VERBS):
        score += 1

    # Length-based minor signal
    if len(action) > 60:
        score += 0  # keep neutral; length alone shouldn't inflate score

    # Clamp to 1–5
    score = max(1, min(5, int(round(score))))

    # Combine with user feedback if provided
    if user_feedback is not None and 1 <= user_feedback <= 5:
        score = int(round((score + user_feedback) / 2))

    # Binary validity for evaluation stage (distinct from schema validation)
    valid = score >= 3

    details = {
        "signals": {
            "has_concrete": any(verb in action for verb in CONCRETE_VERBS),
            "has_vague": any(term in action for term in VAGUE_TERMS),
        },
        "reason": reason,
    }

    return {"valid": valid, "score": score, "details": details}
