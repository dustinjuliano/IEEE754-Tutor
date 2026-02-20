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
