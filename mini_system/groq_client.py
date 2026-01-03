import os
from typing import Dict

try:
    from groq import Groq  # type: ignore
except Exception:
    Groq = None


def _extract_json(text: str) -> Dict[str, str]:
    # Minimal JSON extractor: expect exact JSON or key:value lines
    try:
        import json
        data = json.loads(text)
        return {
            "action": str(data.get("action", "")).strip(),
            "reason": str(data.get("reason", "")).strip(),
        }
    except Exception:
        pass
    # Fallback: look for lines like action: ..., reason: ...
    action, reason = "", ""
    for line in (text or "").splitlines():
        l = line.strip()
        if l.lower().startswith("action:"):
            action = l.split(":", 1)[1].strip()
        elif l.lower().startswith("reason:"):
            reason = l.split(":", 1)[1].strip()
    return {"action": action, "reason": reason}


def propose_action(goal: str) -> Dict[str, str]:
    """Call Groq to propose the next action.

    Returns only {"action","reason"}. Any failure returns empty fields to trigger rejection.
    """
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("LLM_KEY") or os.environ.get("llm_key")
    if not api_key or Groq is None:
        return {"action": "", "reason": ""}

    model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
    client = Groq(api_key=api_key)

    system_prompt = (
        "Respond ONLY with a JSON object: {\"action\": \"...\", \"reason\": \"...\"}. "
        "The action must be concrete and immediately executable. No extra text."
    )
    user_prompt = f"Goal: {goal}"

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_completion_tokens=512,
            top_p=1,
            stream=False,
        )
        content = completion.choices[0].message.content or ""
        result = _extract_json(content)
        return {
            "action": str(result.get("action", "")),
            "reason": str(result.get("reason", "")),
        }
    except Exception:
        return {"action": "", "reason": ""}
