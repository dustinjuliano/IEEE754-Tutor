import random
from src.base_mode import BaseMode
from src.ui import prompt_input, UserQuitException

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

    def run_round(self) -> None:
        target = random.choice(self.questions)
        
        try:
            print("-" * 60)
            print("MODE 7: Subnormals")
            print("-" * 60)
            print(f"Analyze the sequence: {target['seq']}\n")
            
            # Step 1: Type
            print("Is this value Normalized, Denormalized, or Special Case? (Type 'N', 'D', or 'S')")
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
            print("What is the implicit leading bit (1 or 0)?")
            ans_lead = prompt_input("").strip()
            if ans_lead == target['lead']:
                if ans_lead == "0":
                    print("Correct. Denormalized values have an implicit leading 0.\n")
                else:
                    print("Correct. Normalized values have an implicit leading 1.\n")
            else:
                print(f"Incorrect. The leading bit is {target['lead']}.\n")
                
            # Step 3: Unbiased Exponent
            print("What is the true (unbiased) exponent used for calculation (Bias=127)?")
            print("(Hint: For denormals, true exp = 1 - bias)")
            ans_exp = prompt_input("").strip()
            if ans_exp == target['bias_exp']:
                print("Correct.\n")
            else:
                print(f"Incorrect. The true unbiased exponent is {target['bias_exp']}.\n")
            
            
            prompt_input("Press Enter to continue.")
            
        except UserQuitException:
            print("\nExiting mode context...\n")
            return
