from typing import Optional, Dict, Any

try:
    from mini_system.fsm import State, IllegalTransitionError
    from mini_system.llm_client import propose_action as stub_propose_action
    # from mini_system.grok_client import propose_action as grok_propose_action
    from mini_system.groq_client import propose_action as groq_propose_action
    from mini_system.config import load_dotenv
    from mini_system.validator import is_valid
    from mini_system.evaluator import evaluate
    from mini_system.metrics import MetricsCollector
except Exception:
    from fsm import State, IllegalTransitionError
    from llm_client import propose_action as stub_propose_action
    # from grok_client import propose_action as grok_propose_action
    from groq_client import propose_action as groq_propose_action
    from config import load_dotenv
    from validator import is_valid
    from evaluator import evaluate
    from metrics import MetricsCollector


class Orchestrator:
    """Minimal orchestrator implementing the IDLE → DECIDE → EVALUATE → IDLE loop.

    No persistence, metrics, or evaluator yet.
    """

    def __init__(self, proposer=None, provider: str = "stub") -> None:
        # Load .env once at orchestrator init (non-fatal if missing)
        load_dotenv()
        self.state: State = State.IDLE
        self.goal: Optional[str] = None
        self.proposal: Optional[Dict[str, str]] = None
        self.metrics = MetricsCollector()
        # Select proposal function
        if proposer is not None:
            self._propose_action = proposer
        else:
            if provider == "groq":
                self._propose_action = groq_propose_action
            else:
                self._propose_action = stub_propose_action

    def step_idle(self, goal: str) -> State:
        if self.state != State.IDLE:
            raise IllegalTransitionError("Can only receive user input in IDLE state")
        self.goal = goal.strip()
        print(f"[IDLE] Received goal: {self.goal}")
        self.state = State.DECIDE
        return self.state

    def step_decide(self) -> bool:
        if self.state != State.DECIDE:
            raise IllegalTransitionError("Can only decide in DECIDE state")
        proposal = self._propose_action(self.goal or "")
        print(f"[DECIDE] Proposed action: {proposal}")
        is_ok = is_valid(proposal)
        self.metrics.record_llm_response(valid=is_ok)
        if is_ok:
            self.proposal = proposal
            self.state = State.EVALUATE
            return True
        else:
            print("[DECIDE] Rejected LLM output; returning to IDLE")
            self.state = State.IDLE
            return False

    def step_evaluate(self, user_feedback: Optional[int] = None) -> Dict[str, Any]:
        if self.state != State.EVALUATE:
            raise IllegalTransitionError("Can only evaluate in EVALUATE state")
        eval_res = evaluate(self.proposal or {}, user_feedback=user_feedback)
        print(f"[EVALUATE] Result: score={eval_res['score']} valid={eval_res['valid']} details={eval_res['details']}")
        self.metrics.record_evaluation(
            score=int(eval_res["score"]),
            completed=True,
            action_text=(self.proposal or {}).get("action", ""),
        )
        result = {"proposal": self.proposal, "evaluation": eval_res, "metrics": self.metrics.snapshot()}
        self.state = State.IDLE
        return result

    def run_cycle(self, goal: str, user_feedback: Optional[int] = None) -> Dict[str, Any]:
        """Convenience method to run one full cycle.

        Returns final state info and proposal or rejection flag.
        """
        self.step_idle(goal)
        accepted = self.step_decide()
        if not accepted:
            return {"state": self.state.value, "rejected": True}
        eval_result = self.step_evaluate(user_feedback=user_feedback)
        return {"state": self.state.value, **eval_result}
