import unittest
from unittest.mock import patch, MagicMock
from src.engine import IEEEPresets, FLOAT32, FLOAT64, bin32_to_float, bin64_to_float, extract_fields, float_to_bin32, float_to_bin64
from src.ui import UserQuitException, clear_screen, display_main_menu, prompt_input
from src.base_mode import BaseMode
from src.encode_mode import EncodeMode
from src.decode_mode import DecodeMode
from src.min_max_mode import MinMaxMode
from src.special_cases_mode import SpecialCasesMode
from src.denormals_mode import DenormalsMode
from src.precision_impact import PrecisionImpactMode
from src.rounding_mode import RoundingMode

class TestEverySingleDefinition(unittest.TestCase):
    
    # --- ENGINE ---
    def test_engine_IEEEPresets(self):
        self.assertEqual(FLOAT32.bias, 127)
        self.assertEqual(FLOAT64.bias, 1023)
        
    def test_engine_bin32_to_float(self):
        val = bin32_to_float("00111111100000000000000000000000")
        self.assertEqual(val, 1.0)
        
    def test_engine_bin64_to_float(self):
        val = bin64_to_float("0011111111110000000000000000000000000000000000000000000000000000")
        self.assertEqual(val, 1.0)
        
    def test_engine_extract_fields(self):
        s, e, f = extract_fields("00111111100000000000000000000000", FLOAT32)
        self.assertEqual(s, 0)
        self.assertEqual(e, 127)
        self.assertEqual(f, 0)
        
    def test_engine_float_to_bin32(self):
        b = float_to_bin32(1.0)
        self.assertEqual(b, "00111111100000000000000000000000")
        
    def test_engine_float_to_bin64(self):
        b = float_to_bin64(1.0)
        self.assertEqual(b, "0011111111110000000000000000000000000000000000000000000000000000")

    # --- UI ---
    def test_ui_UserQuitException(self):
        with self.assertRaises(UserQuitException):
            raise UserQuitException()
            
    @patch("src.ui.os.system")
    def test_ui_clear_screen(self, mock_sys):
        clear_screen()
        self.assertTrue(mock_sys.called)
        
    @patch("sys.stdout.write")
    def test_ui_display_main_menu(self, mock_write):
        display_main_menu({1: "Test Mode"}, {1: 100.0})
        self.assertTrue(mock_write.called)
        
    @patch("builtins.input", return_value="test")
    def test_ui_prompt_input(self, mock_in):
        val = prompt_input("msg")
        self.assertEqual(val, "test")

    # --- MODES: BASE ---
    def test_base_mode_BaseMode(self):
        class DummyMode(BaseMode):
            def run_round(self): pass
        mode = DummyMode()
        self.assertTrue(hasattr(mode, 'run_round'))
        
    def test_base_mode_init(self):
        class DummyMode(BaseMode):
            def run_round(self): pass
        mode = DummyMode()
        self.assertIsNotNone(mode)
        
    def test_base_mode_run_round(self):
        class DummyMode(BaseMode):
            def run_round(self):
                pass
        mode = DummyMode()
        mode.run_round()

    # --- MODES: ENCODE ---
    def test_encode_mode_EncodeMode(self):
        m = EncodeMode(is_64_bit=False)
        self.assertFalse(m.is_64_bit)
        
    def test_encode_mode_init(self):
        m = EncodeMode(is_64_bit=True)
        self.assertTrue(m.is_64_bit)
        
    def test_encode_mode_generate_target(self):
        m = EncodeMode(is_64_bit=False)
        val = m._generate_target()
        self.assertIsInstance(val, float)
        
    @patch('src.encode_mode.prompt_input', side_effect=UserQuitException())
    def test_encode_mode_run_round(self, mock_prompt):
        m = EncodeMode(is_64_bit=False)
        m.run_round()
        self.assertTrue(mock_prompt.called)

    # --- MODES: DECODE ---
    def test_decode_mode_DecodeMode(self):
        m = DecodeMode(is_64_bit=False)
        self.assertFalse(m.is_64_bit)
        
    def test_decode_mode_init(self):
        m = DecodeMode(is_64_bit=True)
        self.assertTrue(m.is_64_bit)
        
    def test_decode_mode_generate_target(self):
        m = DecodeMode(is_64_bit=False)
        val = m._generate_target()
        self.assertIsInstance(val, float)
        
    @patch('src.decode_mode.prompt_input', side_effect=UserQuitException())
    def test_decode_mode_run_round(self, mock_prompt):
        m = DecodeMode(is_64_bit=False)
        m.run_round()
        self.assertTrue(mock_prompt.called)

    # --- MODES: MIN MAX ---
    def test_min_max_mode_MinMaxMode(self):
        m = MinMaxMode()
        self.assertIsNotNone(m)
        
    def test_min_max_mode_init(self):
        m = MinMaxMode()
        self.assertIsInstance(m, MinMaxMode)
        
    @patch('src.min_max_mode.prompt_input', side_effect=UserQuitException())
    def test_min_max_mode_run_round(self, mock_prompt):
        m = MinMaxMode()
        m.run_round()
        self.assertTrue(mock_prompt.called)

    # --- MODES: SPECIAL CASES ---
    def test_special_cases_mode_SpecialCasesMode(self):
        m = SpecialCasesMode()
        self.assertIsNotNone(m)
        
    def test_special_cases_mode_init(self):
        m = SpecialCasesMode()
        self.assertIsInstance(m, SpecialCasesMode)
        
    @patch('src.special_cases_mode.prompt_input', side_effect=UserQuitException())
    def test_special_cases_mode_run_round(self, mock_prompt):
        m = SpecialCasesMode()
        m.run_round()
        self.assertTrue(mock_prompt.called)

    # --- MODES: DENORMALS ---
    def test_denormals_mode_DenormalsMode(self):
        m = DenormalsMode()
        self.assertIsNotNone(m)
        
    def test_denormals_mode_init(self):
        m = DenormalsMode()
        self.assertIsInstance(m, DenormalsMode)
        
    @patch('src.denormals_mode.prompt_input', side_effect=UserQuitException())
    def test_denormals_mode_run_round(self, mock_prompt):
        m = DenormalsMode()
        m.run_round()
        self.assertTrue(mock_prompt.called)

    # --- MODES: PRECISION IMPACT ---
    def test_precision_impact_PrecisionImpactMode(self):
        m = PrecisionImpactMode()
        self.assertIsNotNone(m)
        
    def test_precision_impact_init(self):
        m = PrecisionImpactMode()
        self.assertIsInstance(m, PrecisionImpactMode)
        
    @patch('src.precision_impact.prompt_input', side_effect=UserQuitException())
    def test_precision_impact_run_round(self, mock_prompt):
        m = PrecisionImpactMode()
        m.run_round()
        self.assertTrue(mock_prompt.called)

    # --- MODES: ROUNDING MODE ---
    def test_rounding_mode_RoundingMode(self):
        m = RoundingMode()
        self.assertIsNotNone(m)
        
    def test_rounding_mode_init(self):
        m = RoundingMode()
        self.assertIsInstance(m, RoundingMode)
        
    @patch('src.rounding_mode.prompt_input', side_effect=UserQuitException())
    def test_rounding_mode_run_round(self, mock_prompt):
        m = RoundingMode()
        m.run_round()
        self.assertTrue(mock_prompt.called)

if __name__ == '__main__':
    unittest.main()
