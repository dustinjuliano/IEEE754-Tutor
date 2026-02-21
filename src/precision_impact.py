import random
from src.base_mode import BaseMode
from src.ui import prompt_input, clear_screen, UserQuitException

class PrecisionImpactMode(BaseMode):
    """Handles Mode 8: Precision Impact."""
    
    def __init__(self):
        super().__init__()
        
        # Format: (Original Seq, Value, Flipped Seq, direction (+ or -), difference)
        self.questions = [
            {
                "orig_seq": "01000000000000000000000000000000",
                "val": "2.0",
                "mod_seq": "01000000000000000000000000000001",
                "dir": "+",
                "diff": "2^-22"
            },
            {
                "orig_seq": "11000000000000000000000000000000",
                "val": "-2.0",
                "mod_seq": "11000000000000000000000000000001",
                "dir": "-",
                "diff": "2^-22"
            },
            {
                "orig_seq": "00111111100000000000000000000000",
                "val": "1.0",
                "mod_seq": "00111111100000000000000000000001",
                "dir": "+",
                "diff": "2^-23"
            }
        ]

    def run_round(self) -> bool:
        target = random.choice(self.questions)
        
        try:
            clear_screen()
            print("-" * 60)
            print("MODE 8: Precision Impact")
            print("-" * 60)
            print(f"Original sequence: {target['orig_seq']} (Value: {target['val']})")
            print("Bit flipped at fraction LSB:")
            print(f"Modified seq:      {target['mod_seq']}\n")
            
            # Step 1: Direction
            print("Determine if the value increased or decreased ('+' or '-'):")
            ans_dir = prompt_input("").strip()
            if ans_dir == target['dir']:
                if ans_dir == "+":
                    print("Correct. The magnitude increased and the number is positive.\n")
                else:
                    print("Correct. The magnitude increased and the number is negative.\n")
            else:
                if target['dir'] == '+':
                    print(f"Incorrect. Flipping a 0 to 1 increases the magnitude, and since the sign is positive (+), the value increases.\n")
                else:
                    print(f"Incorrect. Flipping a 0 to 1 increases the magnitude, but since the sign is negative (-), the value decreases further from zero.\n")
                
            # Step 2: Epsilon Difference
            print("Enter the value of the machine epsilon for this exponent:")
            ans_diff = prompt_input("").strip()
            if ans_diff == target['diff']:
                print(f"Correct. The precision step at this exponent is {target['diff']}.\n")
            else:
                print(f"Incorrect. The precision step is 2^(true exponent - fraction bits), which evaluates to {target['diff']}.\n")
            

            
            prompt_input("Press Enter to continue.")
            
            return True
        except UserQuitException:
            print("\nExiting mode context...\n")
            return False
