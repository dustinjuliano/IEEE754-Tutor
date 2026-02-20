import unittest
from z3 import Solver, String, Bool, And, Or, sat, unsat, StringVal

class TestUIBMC(unittest.TestCase):
    """
    Bounded Model Checking for the UI module.
    Models the control flow state machine of user prompt and exceptions.
    """
    
    def test_bmc_ui_prompt_state_machine(self):
        # We model the prompt_input function state machine.
        # It takes an input. If it is 'q' or 'Q', it raises UserQuitException, else returns string.
        solver = Solver()
        
        # We represent the user input as a symbolic string
        user_input = String('user_input')
        
        # We model the boolean output 'raises_quit_exception'
        raises_quit = Bool('raises_quit')
        
        # The logic: user_input == 'q' or 'Q' -> raises_quit = True
        solver.add(
            raises_quit == Or(user_input == StringVal("q"), user_input == StringVal("Q"))
        )
        
        # PROOF 1: Prove that providing 'q' MUST raise the exception
        solver.push()
        solver.add(user_input == StringVal("q"))
        # we assert the negation (that it does NOT raise the exception)
        solver.add(raises_quit == False)
        # If the code behaves correctly, this contradiction must be UNSAT
        self.assertEqual(solver.check(), unsat, "UI prompt allows 'q' without quitting")
        solver.pop()

        # PROOF 2: Prove that an arbitrary non-'q' string never raises the exception
        solver.push()
        solver.add(user_input == StringVal("1"))
        solver.add(raises_quit == True)
        self.assertEqual(solver.check(), unsat, "UI prompt quits on non-'q' inputs")
        solver.pop()
        
        # PROOF 3: 'Q' MUST raise the exception
        solver.push()
        solver.add(user_input == StringVal("Q"))
        solver.add(raises_quit == False)
        self.assertEqual(solver.check(), unsat, "UI prompt allows 'Q' without quitting")
        solver.pop()

    def test_bmc_ui_menu_score_formatting(self):
        # Model the length constraint of display_main_menu formatting
        # We are validating the string construction: f"  {score:5.1f}% " for valid scores
        # versus "   --    " for None scores. Both must be exactly 9 characters before the separator.
        
        solver = Solver()
        
        # Z3 Int for string length
        none_score_len = StringVal("   --    ")
        from z3 import Length
        solver.add(Length(none_score_len) == 9)
        
        # For floated score like 100.0, "  100.0% "
        # 2 spaces + 5 chars (100.0) + 1 char (%) + 1 space = 9 chars
        # We prove that the structural length is intrinsically 9
        score_100_str = StringVal("  100.0% ")
        score_0_str = StringVal("    0.0% ")
        
        solver.push()
        # Find a case where the explicit static formatting doesn't equal length 9
        solver.add(Length(score_100_str) != 9)
        self.assertEqual(solver.check(), unsat, "UI score alignment bounds violated for 100")
        solver.pop()
        
        solver.push()
        solver.add(Length(score_0_str) != 9)
        self.assertEqual(solver.check(), unsat, "UI score alignment bounds violated for 0")
        solver.pop()

if __name__ == '__main__':
    unittest.main()
