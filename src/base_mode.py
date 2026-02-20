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
    def run_round(self) -> None:
        """
        Executes a single interactive round for this mode.
        Should call prompt_input to interact with the user,
        catch and correctly handle UserQuitException by returning early,
        """
        pass
