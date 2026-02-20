import random
from src.base_mode import BaseMode
from src.ui import prompt_input, clear_screen, UserQuitException

class RoundingMode(BaseMode):
    """Handles Mode 9: Rounding Modes."""
    
    def __init__(self):
        super().__init__()
        
        self.questions = [
            {
                "dec": "0.1",
                "rep": "0.0001100110011...",
                "norm": "1.100110011... x 2^-4",
                "bits": "1001100110011001100110011",
                "g": "1",
                "r": "1",
                "s": "1",
                "decision": "+1",
                "reason": "Guard bit is 1, and (Round | Sticky) is 1, so we round up."
            },
            {
                "dec": "0.05",
                "rep": "0.00001100110011...",
                "norm": "1.100110011... x 2^-5",
                "bits": "1001100110011001100110011",
                "g": "1",
                "r": "1",
                "s": "1",
                "decision": "+1",
                "reason": "Guard bit is 1, and (Round | Sticky) is 1, so we round up."
            }
        ]

    def run_round(self) -> bool:
        target = random.choice(self.questions)
        
        try:
            clear_screen()
            print("-" * 60)
            print("MODE 9: Rounding Modes")
            print("-" * 60)
            print(f"Encode to 32-bit: {target['dec']}")
            print(f"The binary fraction is infinitely repeating: {target['rep']}")
            print(f"Normalized: {target['norm']}\n")
            
            print(f"Fraction bits (first 25): {target['bits']}...")
            print(f"Guard bit: {target['g']}")
            print(f"Round bit: {target['r']}")
            print(f"Sticky bit: {target['s']} (Logical OR of all remaining bits)\n")
            
            print("Determine the rounding decision ('0' to truncate, '+1' to round up):")
            
            ans_dec = prompt_input("").strip()
            if ans_dec == target['decision']:
                print(f"Correct. {target['reason']}\n")
            else:
                print(f"Incorrect. {target['reason']} Decision is {target['decision']}.\n")
            
            
            prompt_input("Press Enter to continue.")
            
            return True
        except UserQuitException:
            print("\nExiting mode context...\n")
            return False
