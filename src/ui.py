"""
UI module handling user input, formatting, and the central context quit mechanism.
"""
import os
from typing import Any, List, Dict

class UserQuitException(Exception):
    """Raised when the user enters 'q' to abort the current context."""
    pass

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_input(message: str) -> str:
    """
    Prompts the user for input, automatically appending the quit instructions 
    and '>>' prompt per the UI mandate.
    
    Raises:
        UserQuitException: if the user types 'q' (case-insensitive).
    """
    if message:
        print(message)
    print("Press `q` to exit.")
    user_input = input(">> ").strip()
    
    if user_input.lower() == 'q':
        raise UserQuitException()
        
    return user_input

def display_main_menu(modes: Dict[int, str]) -> None:
    """
    Prints the main menu and mode descriptions.
    """
    print("============================================================")
    print("                  IEEE 754 TUTOR TERMINAL")
    print("============================================================")
    print("")
    print(" Mode Description")
    print("------------------------------------------------------------")
    
    for mode_id, desc in modes.items():
        print(f" {mode_id}. {desc}")
    
    print("")
