import unittest
from unittest.mock import patch
from src.ui import UserQuitException, prompt_input, display_main_menu, clear_screen

class TestUI(unittest.TestCase):
    def test_prompt_input_normal(self):
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print') as mock_print:
                result = prompt_input("Test message")
                self.assertEqual(result, '1')
                mock_print.assert_any_call("Test message")
                mock_print.assert_any_call("Press `q` to exit.")

    def test_prompt_input_quit(self):
        with patch('builtins.input', return_value='q'):
            with self.assertRaises(UserQuitException):
                prompt_input("Quit test")
                
        with patch('builtins.input', return_value='Q'):
            with self.assertRaises(UserQuitException):
                prompt_input("Quit test upper")

    def test_prompt_input_empty_message(self):
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print') as mock_print:
                result = prompt_input("")
                self.assertEqual(result, '2')
                self.assertEqual(len(mock_print.call_args_list), 1)
                mock_print.assert_called_with("Press `q` to exit.")

    def test_display_main_menu(self):
        import io
        import sys
        
        modes = {
            1: "Mode One",
            2: "Mode Two",
            3: "Mode Three"
        }
        scores = {
            1: 85.5,
            2: 0.0
        }
        
        captured_out = io.StringIO()
        sys.stdout = captured_out
        try:
            display_main_menu(modes, scores)
        finally:
            sys.stdout = sys.__stdout__
            
        output = captured_out.getvalue()
        
        self.assertIn("85.5%", output)
        self.assertIn("  0.0%", output)
        self.assertIn("--", output)
        self.assertIn("1. Mode One", output)
        self.assertIn("2. Mode Two", output)
        self.assertIn("3. Mode Three", output)

    def test_clear_screen(self):
        with patch('os.system') as mock_system:
            clear_screen()
            mock_system.assert_called_once()
