import os
from typing import Optional


def load_dotenv(path: str = ".env") -> None:
    """Minimal .env loader: KEY=VALUE lines, ignore comments and blanks.
    Quotes around values are stripped. Existing environment vars are not overridden.
    """
    try:
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                # Do not override if already set in environment
                if key and (key not in os.environ):
                    os.environ[key] = value
                # Also set upper-case variant if the key is lower-case
                upper = key.upper()
                if upper not in os.environ:
                    os.environ[upper] = os.environ.get(key, value)
    except Exception:
        # Silent failure to keep Phase-1 simple; could log in future
        pass


def get_llm_key() -> Optional[str]:
    # Support both LLM_KEY and llm_key
    return os.environ.get("LLM_KEY") or os.environ.get("llm_key")
