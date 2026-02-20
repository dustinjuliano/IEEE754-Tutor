import random
from src.base_mode import BaseMode
from src.ui import prompt_input, UserQuitException

class SpecialCasesMode(BaseMode):
    """Handles Mode 6: Special Cases (NaN, INF, 0)."""
    
    def __init__(self):
        super().__init__()

        self.questions = [
            {
                "name": "Positive Infinity (+INF)",
                "sign": "0",
                "exp": "1s",
                "frac": "0s"
            },
            {
                "name": "Negative Infinity (-INF)",
                "sign": "1",
                "exp": "1s",
                "frac": "0s"
            },
            {
                "name": "Positive NaN (+NaN)",
                "sign": "0",
                "exp": "1s",
                "frac": "NZ"
            },
            {
                "name": "Negative NaN (-NaN)",
                "sign": "1",
                "exp": "1s",
                "frac": "NZ"
            },
             {
                "name": "Positive Zero (+0)",
                "sign": "0",
                "exp": "0s",
                "frac": "0s"
            },
            {
                "name": "Negative Zero (-0)",
                "sign": "1",
                "exp": "0s",
                "frac": "0s"
            }
        ]

    def run_round(self) -> None:
        target = random.choice(self.questions)
        
        try:
            print("-" * 60)
            print("MODE 6: Special Cases (32-bit)")
            print("-" * 60)
            print(f"Identify the required bit patterns for encoding: {target['name']}\n")
            
            # Step 1: Sign
            print("Step 1: Sign Bit")
            ans_s = prompt_input("")
            if ans_s == target['sign']:
                print("Correct.\n")
            else:
                print(f"Incorrect. The sign bit is {target['sign']}.\n")
                
            # Step 2: Exponent
            print("Step 2: Exponent Pattern")
            print("Should the 8-bit exponent be all 0s, all 1s, or neither? (Type '0s', '1s', or 'N')")
            ans_e = prompt_input("").strip()
            if ans_e.lower() == target['exp'].lower() or \
               ans_e.lower() + "s" == target['exp'].lower(): # allow "0" for "0s"
                print(f"Correct. (All {target['exp']})\n")
            else:
                print(f"Incorrect. The pattern is {target['exp']}.\n")
                
            # Step 3: Fraction
            print("Step 3: Fraction Pattern")
            print("Should the 23-bit fraction be all 0s, or non-zero? (Type '0s' or 'NZ')")
            ans_f = prompt_input("").strip().upper()
            if ans_f == target['frac'] or ans_f + "s" == target['frac'] or ans_f + "S" == target['frac']:
                print(f"Correct. ({'All 0s' if target['frac'] == '0s' else 'Non-Zero'})\n")
            else:
                print(f"Incorrect. The pattern is {target['frac']}.\n")
            
            
            prompt_input("Press Enter to continue.")
            
        except UserQuitException:
            print("\nExiting mode context...\n")
            return
