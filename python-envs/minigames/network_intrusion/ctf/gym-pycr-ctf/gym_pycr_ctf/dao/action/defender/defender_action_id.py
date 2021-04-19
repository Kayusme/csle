from enum import Enum


class DefenderActionId(Enum):
    """
    Enum representing the different defenses
    """
    STOP = 0
    CONTINUE = 1
    UPDATE_STATE = 2
    INITIALIZE_STATE = 3
    RESET_STATE = 4