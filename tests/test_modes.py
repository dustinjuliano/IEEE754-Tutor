import unittest
from unittest.mock import patch, MagicMock
from src.encode_mode import EncodeMode
from src.decode_mode import DecodeMode
from src.min_max_mode import MinMaxMode
from src.special_cases_mode import SpecialCasesMode
from src.denormals_mode import DenormalsMode
from src.precision_impact import PrecisionImpactMode
from src.rounding_mode import RoundingMode

from src.ui import UserQuitException

class TestModes(unittest.TestCase):

    @patch('src.encode_mode.prompt_input', side_effect=UserQuitException())
    def test_encode_mode_quit(self, mock_prompt):
        mode = EncodeMode(is_64_bit=False)
        mode.run_round()
        # Should exit gracefully
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.decode_mode.prompt_input', side_effect=UserQuitException())
    def test_decode_mode_quit(self, mock_prompt):
        mode = DecodeMode(is_64_bit=False)
        mode.run_round()
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.min_max_mode.prompt_input', side_effect=UserQuitException())
    def test_min_max_mode_quit(self, mock_prompt):
        mode = MinMaxMode()
        mode.run_round()
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.special_cases_mode.prompt_input', side_effect=UserQuitException())
    def test_special_cases_mode_quit(self, mock_prompt):
        mode = SpecialCasesMode()
        mode.run_round()
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.denormals_mode.prompt_input', side_effect=UserQuitException())
    def test_denormals_mode_quit(self, mock_prompt):
        mode = DenormalsMode()
        mode.run_round()
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.precision_impact.prompt_input', side_effect=UserQuitException())
    def test_precision_impact_quit(self, mock_prompt):
        mode = PrecisionImpactMode()
        mode.run_round()
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.rounding_mode.prompt_input', side_effect=UserQuitException())
    def test_rounding_mode_quit(self, mock_prompt):
        mode = RoundingMode()
        mode.run_round()
        self.assertEqual(mock_prompt.call_count, 1)

    @patch('src.encode_mode.prompt_input')
    def test_encode_mode_success(self, mock_prompt):
        # We need to mock the random target to a known value
        mode = EncodeMode(is_64_bit=False)
        mode._generate_target = MagicMock(return_value=1.0)
        
        # 1.0 in float32 is sign 0, exp 127 (01111111), frac 0 (00000000000000000000000)
        mock_prompt.side_effect = ['0', '01111111', '0' * 23, '']
        mode.run_round()
        # Ensure it reaches the end and prompts 4 times
        self.assertEqual(mock_prompt.call_count, 4)

