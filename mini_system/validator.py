from typing import Any, Dict


REQUIRED_KEYS = {"action", "reason"}


def is_valid(proposal: Any) -> bool:
    """Validate LLM proposal strictly.

    Requirements:
    - proposal must be a dict
    - keys: "action" and "reason"
    - values: non-empty strings after strip()
    """
    if not isinstance(proposal, dict):
        return False

    # Check required keys present
    if not REQUIRED_KEYS.issubset(proposal.keys()):
        return False

    action = proposal.get("action")
    reason = proposal.get("reason")

    if not isinstance(action, str) or not isinstance(reason, str):
        return False

    if not action.strip() or not reason.strip():
        return False

    return True
