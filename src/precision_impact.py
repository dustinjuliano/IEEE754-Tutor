import random
from src.base_mode import BaseMode
from src.ui import prompt_input, UserQuitException

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

    def run_round(self) -> None:
        target = random.choice(self.questions)
        
        try:
            print("-" * 60)
            print("MODE 8: Precision Impact")
            print("-" * 60)
            print(f"Original sequence: {target['orig_seq']} (Value: {target['val']})")
            print("Bit flipped at fraction LSB:")
            print(f"Modified seq:      {target['mod_seq']}\n")
            
            # Step 1: Direction
            print("Without calculating the exact value, did the value increase or decrease?")
            print("(Type '+' or '-')")
            ans_dir = prompt_input("").strip()
            if ans_dir == target['dir']:
                if ans_dir == "+":
                    print("Correct. The magnitude increased and the number is positive.\n")
                else:
                    print("Correct. The magnitude increased and the number is negative.\n")
            else:
                print(f"Incorrect. It was '{target['dir']}'.\n")
                
            # Step 2: Epsilon Difference
            print("What is the value of this 1 bit difference (the Machine Epsilon for this exponent)?")
            print("(Hint: It is 2^(true exp - 23))")
            ans_diff = prompt_input("").strip()
            if ans_diff == target['diff']:
                print(f"Correct. The precision step at this exponent is {target['diff']}.\n")
            else:
                print(f"Incorrect. It is {target['diff']}.\n")
            
            r_corr, r_att, r_pct = tracker.get_round_score()
            c_corr, c_att, c_pct = tracker.get_cumulative_score(tracker.current_mode_id)
            print(f"Round Score: {r_corr}/{r_att} ({r_pct:.1f}%)")
            print(f"Cumulative Mode Score: {c_corr}/{c_att} ({c_pct:.1f}%)\n")
            
            prompt_input("Press Enter to continue.")
            
        except UserQuitException:
            print("\nExiting mode context...\n")
            return
