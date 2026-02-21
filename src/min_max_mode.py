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
                explanation = "0 for positive" if target['sign'] == "0" else "1 for negative"
                print(f"Incorrect. The sign revolves around {explanation}, so s = {target['sign']}.\n")
                
            # Exponent
            print("Enter the exponent pattern (in binary):")
            ans_e = prompt_input("")
            if ans_e == target['exp']:
                print("Correct.\n")
            else:
                if "Largest" in target['name']:
                    exp_val = 254
                    print(f"Incorrect. The largest valid exponent is all 1s except the LSB (254), representing a true exponent of {exp_val} - {self.preset.bias} = {exp_val - self.preset.bias}.\n")
                else:
                    exp_val = 1
                    print(f"Incorrect. The smallest valid exponent is all 0s except the LSB (1), representing a true exponent of {exp_val} - {self.preset.bias} = {exp_val - self.preset.bias}.\n")
                
            # Fraction
            print("Enter the fraction pattern (in binary):")
            ans_f = prompt_input("")
            if ans_f == target['frac']:
                print("Correct.\n")
            else:
                if "Largest" in target['name']:
                    print(f"Incorrect. The largest magnitude requires the largest fraction: all 1s ({target['frac']}).\n")
                else:
                    print(f"Incorrect. The smallest magnitude requires the smallest fraction: all 0s ({target['frac']}).\n")
            
            
            prompt_input("Press Enter to continue.")
            
            return True
        except UserQuitException:
            print("\nExiting mode context...\n")
            return False
