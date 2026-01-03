from enum import Enum


class IllegalTransitionError(Exception):
    pass


class State(Enum):
    IDLE = "idle"
    DECIDE = "decide"
    EVALUATE = "evaluate"
