import argparse
from typing import Optional
import textwrap

try:
    from mini_system.orchestrator import Orchestrator
except Exception:
    from orchestrator import Orchestrator


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="LLM-Assisted Task Decider (Micro System)")
    p.add_argument("--goal", type=str, help="User goal to run one cycle")
    p.add_argument("--feedback", type=int, choices=range(1, 6), help="Optional user usefulness score (1-5)")
    p.add_argument("--llm", type=str, choices=["stub", "groq"], default="groq", help="LLM provider: stub, or groq")
    return p.parse_args()


def run_once(goal: str, feedback: Optional[int], provider: str) -> None:
    o = Orchestrator(provider=provider)
    result = o.run_cycle(goal, user_feedback=feedback)
    display_result(result)


def run_interactive(provider: str) -> None:
    o = Orchestrator(provider=provider)
    print("LLM-Assisted Task Decider (Micro System) — interactive mode")
    print("Enter a goal (or blank to quit). Optional feedback 1-5 after each cycle.")
    while True:
        goal = input("\nGoal: ").strip()
        if not goal:
            print("Exiting.")
            break
        fb_raw = input("Feedback (1-5, optional): ").strip()
        feedback: Optional[int] = None
        if fb_raw:
            try:
                val = int(fb_raw)
                if 1 <= val <= 5:
                    feedback = val
            except ValueError:
                pass
        result = o.run_cycle(goal, user_feedback=feedback)
        display_result(result)


def display_result(res: dict) -> None:
    def section(title: str) -> None:
        print("\n" + title)
        print("-" * len(title))

    print("\n=== Cycle Result ===")
    print(f"- State: {res.get('state')}")

    proposal = res.get("proposal") or {}
    section("Proposal")
    action = str(proposal.get("action", ""))
    reason = str(proposal.get("reason", ""))
    print("- Action:")
    print(textwrap.fill(action, width=80))
    print("- Reason:")
    print(textwrap.fill(reason, width=80))

    evaluation = res.get("evaluation") or {}
    section("Evaluation")
    print(f"- Valid: {evaluation.get('valid')}")
    print(f"- Score: {evaluation.get('score')}")
    details = evaluation.get("details") or {}
    signals = details.get("signals") or {}
    print(
        f"- Signals: concrete={signals.get('has_concrete')}, vague={signals.get('has_vague')}"
    )

    metrics = res.get("metrics") or {}
    section("Metrics")
    ordered_keys = [
        "llm_valid_output_rate",
        "action_completion_rate",
        "user_usefulness_score_avg",
        "rejection_rate",
        "avg_task_difficulty_vs_completion",
    ]
    for k in ordered_keys:
        if k in metrics:
            print(f"- {k}: {metrics[k]}")


if __name__ == "__main__":
    args = parse_args()
    if args.goal:
        run_once(args.goal, args.feedback, args.llm)
    else:
        run_interactive(args.llm)
