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
    def test_encode_mode_functional_32bit(self, mock_prompt):
        mode = EncodeMode(is_64_bit=False)
        mode._generate_target = MagicMock(return_value=1.5)
        # 1.5 in float32: s=0, e=127 (01111111), f=0.5 (1000...0)
        # Sequence: s, e_bin, f_bin, enter
        mock_prompt.side_effect = ['0', '01111111', '1' + '0'*22, '']
        self.assertTrue(mode.run_round())
        self.assertEqual(mock_prompt.call_count, 4)

    @patch('src.encode_mode.prompt_input')
    def test_encode_mode_functional_64bit(self, mock_prompt):
        mode = EncodeMode(is_64_bit=True)
        mode._generate_target = MagicMock(return_value=-0.75)
        # -0.75 in float64: s=1, e=1022 (01111111110), f=0.5 (1000...0)
        mock_prompt.side_effect = ['1', '01111111110', '1' + '0'*51, '']
        self.assertTrue(mode.run_round())
        self.assertEqual(mock_prompt.call_count, 4)

    @patch('src.decode_mode.prompt_input')
    def test_decode_mode_functional_32bit(self, mock_prompt):
        mode = DecodeMode(is_64_bit=False)
        mode._generate_target = MagicMock(return_value=2.0)
        # 2.0 in float32: 0 10000000 00000000000000000000000
        # Steps: s, e_bits, e_dec (while loop), ue_dec (while loop), lead, final_dec, enter
        # We'll test the while loops with invalid input first
        mock_prompt.side_effect = ['0', '10000000', 'invalid', '128', 'invalid', '1', '1', '2.0', '']
        self.assertTrue(mode.run_round())
        self.assertEqual(mock_prompt.call_count, 9)

    @patch('src.decode_mode.prompt_input')
    def test_decode_mode_functional_64bit(self, mock_prompt):
        mode = DecodeMode(is_64_bit=True)
        mode._generate_target = MagicMock(return_value=-1.0)
        # -1.0 in float64: 1 01111111111 0000...0 (exp=1023)
        mock_prompt.side_effect = ['1', '01111111111', '1023', '0', '1', '-1.0', '']
        self.assertTrue(mode.run_round())
        self.assertEqual(mock_prompt.call_count, 7)

    @patch('src.min_max_mode.prompt_input')
    def test_min_max_mode_functional(self, mock_prompt):
        mode = MinMaxMode()
        # Mock choice to first question: Largest Positive Normalized Number
        with patch('random.choice', return_value=mode.questions[0]):
            mock_prompt.side_effect = ['0', '11111110', '1'*23, '']
            self.assertTrue(mode.run_round())
            self.assertEqual(mock_prompt.call_count, 4)

    @patch('src.special_cases_mode.prompt_input')
    def test_special_cases_mode_functional(self, mock_prompt):
        mode = SpecialCasesMode()
        # Question: Positive Zero
        with patch('random.choice', return_value=mode.questions[0]):
            mock_prompt.side_effect = ['0', '0'*8, '0'*23, '']
            self.assertTrue(mode.run_round())
            self.assertEqual(mock_prompt.call_count, 4)

    @patch('src.denormals_mode.prompt_input')
    def test_denormals_mode_functional(self, mock_prompt):
        mode = DenormalsMode()
        # Question index 0: 0x00400000
        with patch('random.choice', return_value=mode.questions[0]):
            mock_prompt.side_effect = ['D', '1', '-126', '']
            self.assertTrue(mode.run_round())
            self.assertEqual(mock_prompt.call_count, 4)

    @patch('src.precision_impact.prompt_input')
    def test_precision_impact_functional(self, mock_prompt):
        mode = PrecisionImpactMode()
        mock_prompt.side_effect = ['0', '0', '']
        self.assertTrue(mode.run_round())
        self.assertEqual(mock_prompt.call_count, 3)

    @patch('src.rounding_mode.prompt_input')
    def test_rounding_mode_functional(self, mock_prompt):
        mode = RoundingMode()
        with patch('random.choice', return_value=mode.questions[0]):
            mock_prompt.side_effect = ['+1', '']
            self.assertTrue(mode.run_round())
            self.assertEqual(mock_prompt.call_count, 2)

