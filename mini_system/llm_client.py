from typing import Dict


def propose_action(goal: str) -> Dict[str, str]:
    """Deterministic stub that simulates an LLM proposal.

    The LLM is only allowed to suggest a next action and a reason.
    No state changes or evaluation occur here.
    """
    action = f"Break down the goal '{goal}' into actionable steps and pick the first concrete task."
    reason = "Starting with decomposition reduces vagueness and creates immediate momentum."
    return {"action": action, "reason": reason}
