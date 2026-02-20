import random
from src.base_mode import BaseMode
from src.engine import FLOAT32
from src.ui import prompt_input, clear_screen, UserQuitException

class MinMaxMode(BaseMode):
    """Handles Mode 5: Min/Max Value Characteristics."""
    
    def __init__(self):
        super().__init__()
        self.preset = FLOAT32

        self.questions = [
            {
                "name": "Largest Positive Normalized Number",
                "sign": "0",
                "exp": "1" * (self.preset.e_bits - 1) + "0", # e.g. 11111110
                "frac": "1" * self.preset.f_bits
            },
            {
                "name": "Smallest Positive Normalized Number",
                "sign": "0",
                "exp": "0" * (self.preset.e_bits - 1) + "1", # e.g. 00000001
                "frac": "0" * self.preset.f_bits
            },
            {
                "name": "Largest Negative Normalized Number (magnitude)",
                "sign": "1",
                "exp": "1" * (self.preset.e_bits - 1) + "0",
                "frac": "1" * self.preset.f_bits
            },
            {
                "name": "Smallest Negative Normalized Number (magnitude)",
                "sign": "1",
                "exp": "0" * (self.preset.e_bits - 1) + "1",
                "frac": "0" * self.preset.f_bits
            }
        ]

    def run_round(self) -> bool:
        target = random.choice(self.questions)
        
        try:
            clear_screen()
            print("-" * 60)
            print("MODE 5: Min/Max Characteristics (32-bit)")
            print("-" * 60)
            print(f"Identify the characteristics of the {target['name']}.\n")
            
            # Sign
            print("Enter the sign bit (s):")
            ans_s = prompt_input("")
            if ans_s == target['sign']:
                print("Correct.\n")
            else:
                print(f"Incorrect. The sign bit is {target['sign']}.\n")
                
            # Exponent
            print("Enter the exponent pattern (in binary):")
            ans_e = prompt_input("")
            if ans_e == target['exp']:
                print("Correct.\n")
            else:
                print(f"Incorrect. The pattern is {target['exp']}.\n")
                
            # Fraction
            print("Enter the fraction pattern (in binary):")
            ans_f = prompt_input("")
            if ans_f == target['frac']:
                print("Correct.\n")
            else:
                print(f"Incorrect. The pattern is {target['frac']}.\n")
            
            
            prompt_input("Press Enter to continue.")
            
            return True
        except UserQuitException:
            print("\nExiting mode context...\n")
            return False
