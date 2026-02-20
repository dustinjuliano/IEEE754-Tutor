import unittest
import math
from src.engine import (
    FLOAT32, FLOAT64,
    float_to_bin32, float_to_bin64,
    bin32_to_float, bin64_to_float,
    extract_fields
)

class TestEngine(unittest.TestCase):
    def test_float32_conversion(self):
        val = 13.625
        b_str = float_to_bin32(val)
        self.assertEqual(bin32_to_float(b_str), val)
        
        self.assertEqual(float_to_bin32(0.0), "0" * 32)
        self.assertEqual(bin32_to_float("0"*32), 0.0)
        
        nz_str = float_to_bin32(-0.0)
        self.assertEqual(nz_str, "1" + "0"*31)
        self.assertEqual(math.copysign(1.0, bin32_to_float(nz_str)), -1.0)

    def test_float64_conversion(self):
        val = 3.14159
        b_str = float_to_bin64(val)
        self.assertTrue(math.isclose(bin64_to_float(b_str), val, rel_tol=1e-15))
        
        nz_str = float_to_bin64(-0.0)
        self.assertEqual(nz_str, "1" + "0"*63)
        self.assertEqual(math.copysign(1.0, bin64_to_float(nz_str)), -1.0)

    def test_extract_fields(self):
        val = -13.625
        b_str = float_to_bin32(val)
        s, e, f = extract_fields(b_str, FLOAT32)
        self.assertEqual(s, 1)
        
        spaced_str = "1 10000010 10110100000000000000000"
        s, e, f = extract_fields(spaced_str, FLOAT32)
        self.assertEqual(s, 1)
        self.assertEqual(e, int("10000010", 2))
        self.assertEqual(f, int("10110100000000000000000", 2))

    def test_extract_fields_exceptions(self):
        with self.assertRaises(ValueError):
            extract_fields("0", FLOAT32)
        with self.assertRaises(ValueError):
            extract_fields("0"*33, FLOAT32)
            
    def test_bin_to_float_exceptions(self):
        with self.assertRaises(ValueError):
            bin32_to_float("0")
        with self.assertRaises(ValueError):
            bin64_to_float("0")

    def test_special_values_float32(self):
        # Infinity
        inf_str = float_to_bin32(float('inf'))
        self.assertEqual(inf_str, "0" + "1"*8 + "0"*23)
        self.assertEqual(bin32_to_float(inf_str), float('inf'))
        
        # NaN
        nan_str = float_to_bin32(float('nan'))
        # struct.pack('>f', float('nan')) usually gives 0x7fc00000
        self.assertEqual(nan_str[0:9], "011111111")
        self.assertNotEqual(nan_str[9:], "0"*23)
        self.assertTrue(math.isnan(bin32_to_float(nan_str)))

    def test_special_values_float64(self):
        # Infinity
        inf_str = float_to_bin64(float('inf'))
        self.assertEqual(inf_str, "0" + "1"*11 + "0"*52)
        self.assertEqual(bin64_to_float(inf_str), float('inf'))
        
        # NaN
        nan_str = float_to_bin64(float('nan'))
        self.assertEqual(nan_str[0:12], "011111111111")
        self.assertNotEqual(nan_str[12:], "0"*52)
        self.assertTrue(math.isnan(bin64_to_float(nan_str)))

    def test_extract_fields_no_fraction(self):
        # Create a mock preset with 0 fraction bits to test the 'if f_str else 0' branch
        from src.engine import IEEEPresets
        tiny_preset = IEEEPresets(bias=1, e_bits=2, f_bits=0, total_bits=3)
        s, e, f = extract_fields("110", tiny_preset)
        self.assertEqual(s, 1)
        self.assertEqual(e, 2)
        self.assertEqual(f, 0)
