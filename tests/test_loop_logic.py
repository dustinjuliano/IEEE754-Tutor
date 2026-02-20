import unittest
from unittest.mock import patch
from src.denormals_mode import DenormalsMode
from src.ui import UserQuitException

class TestLoopLogic(unittest.TestCase):
    def test_denormals_mode_success_returns_true(self):
        mode = DenormalsMode()
        # Mock random to pick a stable question
        import random
        question = mode.questions[0]
        
        with patch('random.choice', return_value=question):
            # Step 1: D, Step 2: 0, Step 3: -126, Final: Enter
            with patch('src.denormals_mode.prompt_input', side_effect=['D', '0', '-126', '']):
                result = mode.run_round()
                self.assertTrue(result)

    def test_denormals_mode_quit_returns_false(self):
        mode = DenormalsMode()
        import random
        question = mode.questions[0]
        
        with patch('random.choice', return_value=question):
            # User quits at the first step
            with patch('src.denormals_mode.prompt_input', side_effect=UserQuitException()):
                result = mode.run_round()
                self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
