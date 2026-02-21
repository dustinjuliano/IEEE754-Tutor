import random
from src.base_mode import BaseMode
from src.ui import prompt_input, clear_screen, UserQuitException

class DenormalsMode(BaseMode):
    """Handles Mode 7: Subnormals (Normalized vs Denormalized)."""
    
    def __init__(self):
        super().__init__()

        self.questions = [
            {
                "seq": "00000000011000000000000000000000",
                "type": "D",
                "reason": "The exponent is all 0s and fraction is non-zero.",
                "lead": "0",
                "bias_exp": "-126" # 1 - 127
            },
            {
                "seq": "01000000011000000000000000000000",
                "type": "N",
                "reason": "The exponent is neither all 0s nor all 1s.",
                "lead": "1",
                "bias_exp": "1" # 128 - 127
            },
            {
                "seq": "01111111100000000000000000000000",
                "type": "S",
                "reason": "The exponent is all 1s and the fraction is all 0s (+INF).",
                "lead": "None",
                "bias_exp": "N/A"
            }
        ]

    def run_round(self) -> bool:
        target = random.choice(self.questions)
        
        try:
            clear_screen()
            print("-" * 60)
            print("MODE 7: Subnormals")
            print("-" * 60)
            print(f"Analyze the sequence: {target['seq']}\n")
            
            # Step 1: Type
            print("Enter the value type ('N' for Normalized, 'D' for Denormalized, or 'S' for Special Case):")
            ans_type = prompt_input("").strip().upper()
            if ans_type == target['type']:
                print(f"Correct. {target['reason']}\n")
            else:
                print(f"Incorrect. It is type '{target['type']}'. {target['reason']}\n")
            
            if target['type'] == 'S':
                # Special cases don't ask about leading bit or unbiased exponent generally.
                prompt_input("Press Enter to continue.")
                return

            # Step 2: Leading Bit
            print("Enter the implicit leading bit:")
            ans_lead = prompt_input("").strip()
            if ans_lead == target['lead']:
                if ans_lead == "0":
                    print("Correct. Denormalized values have an implicit leading 0.\n")
                else:
                    print("Correct. Normalized values have an implicit leading 1.\n")
            else:
                if target['lead'] == "0":
                    print("Incorrect. Denormalized values have an implicit leading 0 because their exponent is minimum (0).\n")
                else:
                    print("Incorrect. Normalized values have an implicit leading 1 per the IEEE 754 standard.\n")
                
            # Step 3: Unbiased Exponent
            print("Enter the true (unbiased) exponent (Bias=127):")
            ans_exp = prompt_input("").strip()
            if ans_exp == target['bias_exp']:
                print("Correct.\n")
            else:
                if target['type'] == 'D':
                    print(f"Incorrect. Subnormals have a fixed true exponent of 1 - bias (127), so 1 - 127 = {target['bias_exp']}.\n")
                else:
                    print(f"Incorrect. Normalized true exponent is biased exponent - bias (127), resulting in {target['bias_exp']}.\n")
            
            
            prompt_input("Press Enter to continue.")
            
            return True
        except UserQuitException:
            print("\nExiting mode context...\n")
            return False
