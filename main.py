import sys
from src.ui import display_main_menu, prompt_input, clear_screen, UserQuitException

from src.encode_mode import EncodeMode
from src.decode_mode import DecodeMode
from src.min_max_mode import MinMaxMode
from src.special_cases_mode import SpecialCasesMode
from src.denormals_mode import DenormalsMode
from src.precision_impact import PrecisionImpactMode
from src.rounding_mode import RoundingMode

AVAILABLE_MODES = {
    1: "32-bit (Single) Encoding (Decimal -> Binary)",
    2: "32-bit (Single) Decoding (Binary -> Decimal)",
    3: "64-bit (Double) Encoding (Decimal -> Binary)",
    4: "64-bit (Double) Decoding (Binary -> Decimal)",
    5: "Min/Max Value Characteristics",
    6: "Special Cases (NaN, INF, 0)",
    7: "Subnormals (Normalized vs Denormalized)",
    8: "Precision Impact",
    9: "Rounding Modes",
}

def main():
    
    while True:
        clear_screen()
        display_main_menu(AVAILABLE_MODES)
        
        try:
            choice_str = prompt_input("Select a mode (number) [q to quit]: ")
            if not choice_str:
                continue
                
            choice = int(choice_str)
            if choice not in AVAILABLE_MODES:
                print(f"\nInvalid choice. Please select a mode from 1 to {len(AVAILABLE_MODES)}.")
                prompt_input("\nPress Enter to continue.")
                continue
            
            if choice == 1:
                mode = EncodeMode(is_64_bit=False)
            elif choice == 2:
                mode = DecodeMode(is_64_bit=False)
            elif choice == 3:
                mode = EncodeMode(is_64_bit=True)
            elif choice == 4:
                mode = DecodeMode(is_64_bit=True)
            elif choice == 5:
                mode = MinMaxMode()
            elif choice == 6:
                mode = SpecialCasesMode()
            elif choice == 7:
                mode = DenormalsMode()
            elif choice == 8:
                mode = PrecisionImpactMode()
            elif choice == 9:
                mode = RoundingMode()
            else:
                print(f"\nMode {choice} is not yet implemented.")
                prompt_input("\nPress Enter to return to the menu.")
                continue
                
            mode.run_round()
            
        except UserQuitException:
            print("\nExiting IEEE 754 Tutor. Goodbye!")
            sys.exit(0)
        except ValueError:
            print("\nPlease enter a valid number.")
            try:
                prompt_input("\nPress Enter to continue.")
            except UserQuitException:
                sys.exit(0)
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()
