"""
Mathematical engine for IEEE 754 precision conversions and bit manipulation.
"""
import struct
from dataclasses import dataclass
from typing import Tuple

@dataclass
class IEEEPresets:
    bias: int
    e_bits: int
    f_bits: int
    total_bits: int

FLOAT32 = IEEEPresets(bias=127, e_bits=8, f_bits=23, total_bits=32)
FLOAT64 = IEEEPresets(bias=1023, e_bits=11, f_bits=52, total_bits=64)

def float_to_bin32(value: float) -> str:
    """Convert a python float to a 32-bit binary string representation."""
    if value == 0.0:
        # Check signed zero
        import math
        if math.copysign(1.0, value) < 0:
            return "1" + "0" * 31
        return "0" * 32
        
    [bits] = struct.unpack('>I', struct.pack('>f', value))
    return f"{bits:032b}"

def float_to_bin64(value: float) -> str:
    """Convert a python float to a 64-bit binary string representation."""
    if value == 0.0:
        import math
        if math.copysign(1.0, value) < 0:
            return "1" + "0" * 63
        return "0" * 64
        
    [bits] = struct.unpack('>Q', struct.pack('>d', value))
    return f"{bits:064b}"

def bin32_to_float(binary_str: str) -> float:
    """Convert a 32-bit binary string to a python float."""
    binary_str = binary_str.replace(" ", "")
    if len(binary_str) != 32:
        raise ValueError("bin32_to_float requires exactly 32 bits.")
        
    bits = int(binary_str, 2)
    [value] = struct.unpack('>f', struct.pack('>I', bits))
    return value

def bin64_to_float(binary_str: str) -> float:
    """Convert a 64-bit binary string to a python float."""
    binary_str = binary_str.replace(" ", "")
    if len(binary_str) != 64:
        raise ValueError("bin64_to_float requires exactly 64 bits.")
        
    bits = int(binary_str, 2)
    [value] = struct.unpack('>d', struct.pack('>Q', bits))
    return value

def extract_fields(binary_str: str, preset: IEEEPresets) -> Tuple[int, int, int]:
    """
    Extracts the Sign, Exponent, and Fraction from a raw binary string.
    Returns integers representing the fields.
    """
    clean_str = binary_str.replace(" ", "")
    if len(clean_str) != preset.total_bits:
        raise ValueError(f"Expected {preset.total_bits} bits, got {len(clean_str)}")
        
    s_end = 1
    e_end = s_end + preset.e_bits
    
    s_str = clean_str[0:s_end]
    e_str = clean_str[s_end:e_end]
    f_str = clean_str[e_end:]
    
    s = int(s_str, 2)
    e = int(e_str, 2)
    f = int(f_str, 2) if f_str else 0
    
    return s, e, f
