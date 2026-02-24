import random
import math
from src.base_mode import BaseMode
from src.engine import (
    FLOAT32, FLOAT64, IEEEPresets,
    float_to_bin32, float_to_bin64, extract_fields,
    bin32_to_float, bin64_to_float
)
from src.ui import prompt_input, clear_screen, UserQuitException

class DecodeMode(BaseMode):
    """Handles Mode 2 (32-bit) and Mode 4 (64-bit) Decoding."""
    
    def __init__(self, is_64_bit: bool = False):
        super().__init__()
        self.preset = FLOAT64 if is_64_bit else FLOAT32
        self.is_64_bit = is_64_bit
        self.mode_name = "64-bit Decoding" if is_64_bit else "32-bit Decoding"

    def _generate_target(self) -> float:
        sign = random.choice([-1, 1])
        base = random.randint(1, 100)
        frac = random.choice([0.0, 0.25, 0.5, 0.75, 0.125])
        return sign * (base + frac)

    def run_round(self) -> bool:
        target_val = self._generate_target()
        
        if self.is_64_bit:
            binary_str = float_to_bin64(target_val)
        else:
            binary_str = float_to_bin32(target_val)
            
        gt_s, gt_e, gt_f = extract_fields(binary_str, self.preset)
        
        try:
            clear_screen()
            print("-" * 60)
            print(f"MODE: {self.mode_name}")
            print("-" * 60)
            print(f"Target Sequence: {binary_str}\n")
            
            # Step 1: Sign
            print("Step 1: Extract Bits")
            print("Enter the sign bit (s):")
            ans_s = prompt_input("")
            if ans_s == str(gt_s):
                print(f"Correct. ({'Negative' if gt_s == 1 else 'Positive'})\n")
            else:
                print(f"Incorrect. The sign is 1 for negative and 0 for positive, so s = {gt_s}.\n")
                
            # Step 1b: Exponent extraction
            gt_e_bin = f"{gt_e:0{self.preset.e_bits}b}"
            print(f"Enter the exponent sequence:")
            ans_e = prompt_input("")
            if ans_e == gt_e_bin:
                print("Correct.\n")
            else:
                print(f"Incorrect. The exponent is the {self.preset.e_bits} bits following the sign bit: {gt_e_bin}.\n")
                
            # Step 2: Exponent Value
            print("Step 2: Exponent Value")
            print(f"Enter the decimal value of the biased exponent `{gt_e_bin}`:")
            while True:
                ans_e_dec = prompt_input("")
                try:
                    int_ans_e = int(ans_e_dec)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
            
            if int_ans_e == gt_e:
                print("Correct.\n")
            else:
                print(f"Incorrect. The decimal value of the binary sequence {gt_e_bin} is {gt_e}.\n")

            unbiased_e = gt_e - self.preset.bias
            print(f"Enter the unbiased true exponent:")
            while True:
                ans_ue = prompt_input("")
                try:
                    int_ans_ue = int(ans_ue)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
            
            if int_ans_ue == unbiased_e:
                print(f"Correct. (True Exponent = {unbiased_e})\n")
            else:
                print(f"Incorrect. True exponent is biased exponent - bias ({self.preset.bias}), so {gt_e} - {self.preset.bias} = {unbiased_e}.\n")
                
            # Step 3: Final Value
            print("Step 3: Final Value")
            print("Enter the implicit leading bit:")
            # For this simple mock we assume normalized, meaning e != 0.
            # Real logic would check if it's subnormal, but our _generate_target avoids them.
            ans_lead = prompt_input("")
            if ans_lead == "1":
                print("Correct. (Normalized value)\n")
            else:
                print("Incorrect. It is normalized, thus 1.\n")
                
            print("Enter the final decimal value:")
            ans_dec = prompt_input("")
            try:
                if math.isclose(float(ans_dec), target_val, rel_tol=1e-5):
                    print("Correct.\n")
                else:
                    print(f"Incorrect. The value is (-1)^sign * (1 + fraction) * 2^(true exponent), so (-1)^{gt_s} * (1 + {gt_f / (2**self.preset.f_bits)}) * 2^{unbiased_e} = {target_val}.\n")
            except ValueError:
                print(f"Incorrect format. The value is (-1)^sign * (1 + fraction) * 2^(true exponent), so {target_val}.\n")

            
            prompt_input("Press Enter to continue.")
            
            return True
        except UserQuitException:
            print("\nExiting mode context...\n")
            return False
