# LLM-Assisted Task Decider (Mini System)

A minimal, 3-state micro-system that takes a user goal, asks an LLM (stubbed), validates the proposal, evaluates usefulness, records metrics, and returns to idle for the next goal.

- Deterministic control: FSM + validation + evaluation + metrics
- No databases, no complex UI
- Focused on system architecture and learning

---

## Quick Start

### Prerequisites
- Python 3.11+
- PowerShell (Windows) or a shell

### Setup
```powershell
# From project root
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run (single cycle)
```powershell
python -m mini_system.main --goal "design a roadmap to learn llm" --llm stub
```

### Run (interactive loop)
```powershell
python -m mini_system.main --interactive --llm stub
```

### Run via helper script (asks for goal)
```powershell
./run.ps1
```

---

## Architecture Overview

### Finite State Machine (FSM)
States: `IDLE → DECIDE → EVALUATE → IDLE`

```
IDLE ──(user_input)──▶ DECIDE ──(valid_action)──▶ EVALUATE ──(done)──▶ IDLE
            └──(invalid_action)──────────────┘
```

- Allowed transitions are enforced; illegal transitions raise errors.
- LLM suggestions do not change state directly—only validated orchestration does.

### Control Loop (Sense → Decide → Act → Evaluate)
- Sense: read user input (goal)
- Decide: LLM proposes an action
- Act: present action
- Evaluate: score usefulness (binary + scalar) and update metrics

### Modules
- mini_system/fsm.py: State enum + transition error
- mini_system/orchestrator.py: Implements the control loop and transitions
- mini_system/llm_client.py: Deterministic stub LLM returning `{action, reason}`
- mini_system/validator.py: Schema validation (action/reason non-empty)
- mini_system/evaluator.py: Heuristic evaluation (`valid`, `score 1–5`, signals)
- mini_system/metrics.py: In-memory metrics collector + snapshot
- mini_system/main.py: CLI entry (single-cycle and interactive)
- mini_system/config.py: `.env` loading helper (minimal)

---

## Data Contract: LLM Output
LLM proposals must match this schema. Invalid outputs are rejected.
```json
{
  "action": "string",
  "reason": "string"
}
```

---

## Evaluation & Metrics

### Evaluation
- `valid`: binary fitness-for-purpose determination
- `score`: scalar usefulness (1–5)
- `details.signals`: simple signals for concrete vs vague cues + feedback blend

### Metrics (tracked per cycle)
- `llm_valid_output_rate`
- `action_completion_rate`
- `user_usefulness_score_avg`
- `rejection_rate`
- `avg_task_difficulty_vs_completion`

---

## Repository Structure
```
mini_system/
  fsm.py
  orchestrator.py
  llm_client.py
  validator.py
  evaluator.py
  metrics.py
  main.py
  config.py
run.ps1
README.md
requirements.txt
```

---

## Configuration
- Environment variables can be set in a `.env` file; loaded by `mini_system/config.py`.
- Phase 1 keeps configuration minimal and local.

---

## Roadmap (Next Steps)
- Validator usefulness guard (reject vague actions at DECIDE)
- Bounded retries in DECIDE (e.g., max 1–2 attempts)
- Event logging hooks (`USER_INPUT`, `LLM_RESPONSE`, `USER_FEEDBACK`)
- Unit tests for validator, evaluator, and orchestrator transitions
- Metrics persistence (CSV/JSON) for session analyses

---

## Notes
- Current LLM provider: stub only; external providers are intentionally removed for Phase 1.
- `.gitignore` excludes virtual environments, env files, and `docs/`.# LLM-Assisted Task Decider (Mini System)

A minimal, 3-state micro-system that takes a user goal, asks an LLM (stubbed), validates the proposal, evaluates usefulness, records metrics, and returns to idle for the next goal.

- Deterministic control: FSM + validation + evaluation + metrics
- No databases, no complex UI
- Focused on system architecture and learning

---

## Quick Start

### Prerequisites
- Python 3.11+
- PowerShell (Windows) or a shell

### Setup
```powershell
# From project root
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run (single cycle)
```powershell
python -m mini_system.main --goal "design a roadmap to learn llm" --llm stub
```

### Run (interactive loop)
```powershell
python -m mini_system.main --interactive --llm stub
```

### Run via helper script (asks for goal)
```powershell
./run.ps1
```

---