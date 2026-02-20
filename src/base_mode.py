from abc import ABC, abstractmethod

class BaseMode(ABC):
    """
    Abstract base class for all IEEE 754 Tutor educational modes.
    """
    def __init__(self):
        # We can store the mode name or ID here if needed, 
        # but the main menu handles routing.
        pass
        
    @abstractmethod
    def run_round(self) -> bool:
        """
        Executes a single interactive round for this mode.
        Should call prompt_input to interact with the user,
        handle UserQuitException by returning False,
        and return True upon successful completion of a round.
        """
        pass
