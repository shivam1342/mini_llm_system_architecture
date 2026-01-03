# LLM-Assisted Task Decider (Mini System)# LLM-Assisted Task Decider (Mini System)



- `.gitignore` excludes venvs, env files, and `docs/`.- Current LLM provider: `stub` only. External clients previously explored are intentionally removed for now.## Notes- Metrics persistence (CSV/JSON) for session analysis- Unit tests for validator, evaluator, and orchestrator transitions- Event logging hooks for `USER_INPUT`, `LLM_RESPONSE`, `USER_FEEDBACK`- Bounded retries in `DECIDE` (e.g., max 1–2; no infinite loops)- Usefulness pre-check in validator (reject vague actions earlier)## Roadmap (Phase 1 → Next)```requirements.txtrun.ps1└── main.py├── config.py├── metrics.py├── evaluator.py├── validator.py├── llm_client.py├── orchestrator.py├── fsm.pymini_system/```## Repository Structure- Future providers can read keys via `mini_system/config.py`.- Place environment variables in `.env` (optional). Current Phase 1 uses the LLM stub and does not require external keys.## Configuration```.\\run.ps1```powershellPowerShell helper:```python -m mini_system.main --interactive --llm stub```powershellInteractive run:```python -m mini_system.main --goal "design dsa road map" --feedback 1 --llm stub```powershellSingle-cycle run:## Usage Examples  - Avg task difficulty vs completion  - Rejection rate (bad LLM outputs)  - User usefulness score avg  - Action completion rate  - LLM valid output rate- Metrics tracked:- Scalar usefulness score: `1–5`- Binary validity: `True/False` (based on signals + schema)## Evaluation & MetricsIf the output is missing fields or is empty → reject and return to `IDLE`.```}  "reason": "string"  "action": "string",{```json## Data Contract (LLM Output)- `mini_system/config.py`: optional `.env` loading- `mini_system/main.py`: CLI (single + interactive) with readable output- `mini_system/metrics.py`: in-memory metrics collector- `mini_system/evaluator.py`: usefulness scoring + signals- `mini_system/validator.py`: schema validation (string, non-empty)- `mini_system/llm_client.py`: deterministic stub `propose_action(goal)` returning `{action, reason}`- `mini_system/orchestrator.py`: IDLE → DECIDE → EVALUATE → IDLE loop- `mini_system/fsm.py`: `State` enum and `IllegalTransitionError`### Modules```Evaluate: score (1–5), valid/invalid; update metricsAct     : present proposal to userDecide  : LLM stub proposes {action, reason}Sense   : read user input goal```### Control Loop (Sense → Decide → Act → Evaluate)- Actions: `propose_action(goal)`, `present_action(proposal)`, `evaluate(proposal, feedback)`- Guards: `is_valid(proposal)` (schema; usefulness pre-check planned)- Events: `USER_INPUT`, `LLM_RESPONSE`, `USER_FEEDBACK`- States: `IDLE`, `DECIDE`, `EVALUATE````             └──(invalid_action)──────────────┘IDLE ──(user_input)──▶ DECIDE ──(valid_action)──▶ EVALUATE ──(done)──▶ IDLE```### Finite State Machine (FSM)## Architecture```.\\run.ps1# Prompts for goal and runs one cycle```powershell### Run via PowerShell helper```python -m mini_system.main --interactive --llm stub```powershell### Run (interactive)```python -m mini_system.main --goal "design a roadmap to learn llm" --feedback 3 --llm stub# Provide goal and optional feedback (1–5)```powershell### Run (single cycle)```pip install -r requirements.txt.venv\\Scripts\\Activate.ps1python -m venv .venv# From project root```powershell### Setup- PowerShell (for `run.ps1`, optional)- Python 3.11+### Prerequisites## Quick Start- CLI runner and PowerShell helper- In-memory metrics for Phase 1- Heuristic evaluation (binary valid + scalar score 1–5)- Strict schema validation of LLM output- 3 explicit states: IDLE → DECIDE → EVALUATEA minimal, deterministic micro-system that takes a user goal, asks a constrained LLM to propose an action, validates it, evaluates usefulness, and records simple metrics.
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
- `mini_system/fsm.py`: State enum + transition error
- `mini_system/orchestrator.py`: Implements the control loop and transitions
- `mini_system/llm_client.py`: Deterministic stub LLM returning `{action, reason}`
- `mini_system/validator.py`: Schema validation (action/reason non-empty)
- `mini_system/evaluator.py`: Heuristic evaluation (`valid`, `score 1–5`, signals)
- `mini_system/metrics.py`: In-memory metrics collector + snapshot
- `mini_system/main.py`: CLI entry (single-cycle and interactive)
- `mini_system/config.py`: `.env` loading helper (minimal)

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

## Usage Examples
Single-cycle example (CLI):
```powershell
python -m mini_system.main --goal "design a roadmap to learn llm" --llm stub
```
Interactive example:
```powershell
python -m mini_system.main --interactive --llm stub
```
Helper script:
```powershell
./run.ps1
```

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
- Current LLM provider: `stub` only; external providers are intentionally removed for Phase 1.
- `.gitignore` excludes virtual environments, env files, and `docs/`.
