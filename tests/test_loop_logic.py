import unittest
from main import main
from src.ui import UserQuitException
from src.denormals_mode import DenormalsMode
from unittest.mock import patch, MagicMock

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

    @patch('main.prompt_input')
    @patch('main.clear_screen')
    @patch('main.display_main_menu')
    def test_main_loop_logic(self, mock_menu, mock_clear, mock_prompt):
        # We simulate:
        # 1. Invalid input (Value Error)
        # 2. Invalid mode number
        # 3. Mode 1 selection followed by immediate quit of mode
        # 4. Quit global application
        
        # Choice strings for prompt_input
        # 'invalid' -> ValueError -> prompts "Press Enter to continue" (needs '')
        # '99'      -> Invalid choice -> prompts "Press Enter to continue" (needs '')
        # ''        -> Continue -> loops menu
        # '1'       -> EncodeMode(False) -> run_round returns False -> loops menu
        # 'q'       -> UserQuitException -> Exit
        
        mock_prompt.side_effect = ['invalid', '', '99', '', '', '1', UserQuitException()]
        
        # For mode selection '1', we need to mock EncodeMode.run_round to return False immediately
        with patch('main.EncodeMode') as mock_encode:
            mock_mode_instance = MagicMock()
            mock_mode_instance.run_round.return_value = False
            mock_encode.return_value = mock_mode_instance
            
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

    @patch('main.prompt_input')
    @patch('main.clear_screen')
    @patch('main.display_main_menu')
    def test_main_loop_all_modes_routing(self, mock_menu, mock_clear, mock_prompt):
        # Verify all modes 1-9 are routed correctly
        # We'll mock run_round to return False so it doesn't loop forever in a mode.
        mock_prompt.side_effect = ['1', '2', '3', '4', '5', '6', '7', '8', '9', UserQuitException()]
        
        with patch('main.EncodeMode') as m1, \
             patch('main.DecodeMode') as m2, \
             patch('main.MinMaxMode') as m5, \
             patch('main.SpecialCasesMode') as m6, \
             patch('main.DenormalsMode') as m7, \
             patch('main.PrecisionImpactMode') as m8, \
             patch('main.RoundingMode') as m9:
            
            for m in [m1, m2, m3 := MagicMock(), m4 := MagicMock(), m5, m6, m7, m8, m9]:
                # Handle m3 and m4 which are also just Encode/Decode with is_64_bit=True
                pass

            # Redefine routing mocks more cleanly
            inst = MagicMock()
            inst.run_round.return_value = False
            
            m1.return_value = inst
            m2.return_value = inst
            m5.return_value = inst
            m6.return_value = inst
            m7.return_value = inst
            m8.return_value = inst
            m9.return_value = inst
                
            with self.assertRaises(SystemExit):
                main()
            
            # Verify they were called
            self.assertEqual(m1.call_count, 2) # Mode 1 and 3
            self.assertEqual(m2.call_count, 2) # Mode 2 and 4
            self.assertTrue(m5.called)
            self.assertTrue(m6.called)
            self.assertTrue(m7.called)
            self.assertTrue(m8.called)
            self.assertTrue(m9.called)

if __name__ == '__main__':
    unittest.main()
