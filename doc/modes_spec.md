# Educational Modes & UI Mockups

This document details the interface flow and UX for all 9 educational modes in the IEEE 754 Tutor.

---

## Main Menu View

The main menu is the entry point, listing the available modes along with the user's current cumulative accuracy across historical attempts.

```text
============================================================
                  IEEE 754 TUTOR TERMINAL
============================================================

Accuracy | Mode Description
---------+--------------------------------------------------
  85.0%  | 1. 32-bit (Single) Encoding (Decimal -> Binary)
  90.5%  | 2. 32-bit (Single) Decoding (Binary -> Decimal)
    --   | 3. 64-bit (Double) Encoding
    --   | 4. 64-bit (Double) Decoding
 100.0%  | 5. Min/Max Value Characteristics
    --   | 6. Special Cases (NaN, INF, 0)
    --   | 7. Subnormals (Normalized vs Denormalized)
    --   | 8. Precision Impact
    --   | 9. Rounding Modes

Press `q` to exit.
>> _
```

---

## 1. 32-bit Encoding Mode (Decimal -> Binary)

**Objective**: Convert a decimal number into its 32-bit binary IEEE 754 representation.


```text
------------------------------------------------------------
MODE 1: 32-bit Encoding
------------------------------------------------------------
Target Value: -13.625

Step 1: Determine the Sign Bit (s)
Is the number positive (0) or negative (1)?
Press `q` to exit.
>> 1
Correct. [s = 1]

Step 2: Determine the Exponent (e)
Convert the absolute value to binary: 13.625 -> 1101.101
Normalize the binary value: 1.101101 x 2^3
Calculate unbiased exponent: 3
Calculate biased exponent: 3 + 127 = 130
Enter the 8-bit biased exponent in binary:
Press `q` to exit.
>> 10000010
Correct. [e = 10000010]

Step 3: Determine the Fraction (f)
Extract the fractional part after normalization: 101101
Enter the 23-bit fraction in binary (pad with 0s):
Press `q` to exit.
>> 10110100000000000000000
Correct. [f = 10110100000000000000000]

Results:
Sign:     [1]
Exponent: [10000010]
Fraction: [10110100000000000000000]
Full Binary: 11000001010110100000000000000000

Round Score: 3/3 (100.0%)
Cumulative Mode Score: 3/3 (100.0%)

Press Enter to continue.
Press `q` to exit.
>> _
```

---

## 2. 32-bit Decoding Mode (Binary -> Decimal)

**Objective**: Convert a given 32-bit sequence back to decimal representation.


```text
------------------------------------------------------------
MODE 2: 32-bit Decoding
------------------------------------------------------------
Target Sequence: 01000001101100000000000000000000

Step 1: Extract Bits
What is the Sign Bit (0 or 1)?
Press `q` to exit.
>> 0
Correct. (Positive)

What is the 8-bit Exponent sequence?
Press `q` to exit.
>> 10000011
Correct.

Step 2: Exponent Value
What is the decimal value of the biased exponent `10000011`?
Press `q` to exit.
>> 131
Correct.
What is the unbiased true exponent?
Press `q` to exit.
>> 4
Correct. (True Exponent = 4)

Step 3: Final Value
What is the implicit leading bit (1 or 0, since e is not 0)?
Press `q` to exit.
>> 1
Correct. (Normalized value)
Evaluate: +1 * (1 + 0.375) * 2^4
Enter the final decimal value:
Press `q` to exit.
>> 22.0
Correct.

Round Score: 5/5 (100.0%)
Cumulative Mode Score: 15/15 (100.0%)
```

---

## 3. 64-bit Encoding Mode (Decimal -> Binary)

**Objective**: Convert a decimal number into its 64-bit binary representation.
(Similar flow to Mode 1, but with 11-bit biased exponent (bias 1023) and 52-bit fraction).

```text
------------------------------------------------------------
MODE 3: 64-bit Encoding
------------------------------------------------------------
Target Value: 3.14159

Step 1: Determine the Sign Bit (s)
Is the number positive (0) or negative (1)?
Press `q` to exit.
>> 0
...
[Steps 2 and 3 omitted for brevity, but matches Mode 1 flow with larger fields]
...
Full Binary: 01000000000010010010000111111011...
```

---

## 4. 64-bit Decoding Mode (Binary -> Decimal)

**Objective**: Convert a 64-bit sequence to decimal representation.
(Similar flow to Mode 2, using 64-bit dimensions).

```text
------------------------------------------------------------
MODE 4: 64-bit Decoding
------------------------------------------------------------
Target Sequence: 001111111111000000000000...
...
[Extracts s(1), e(11), f(52) through same step-by-step logic as Mode 2]
```

---

## 5. Min/Max Value Characteristics

**Objective**: Train users on the standard extreme values for standard precision floats.

```text
------------------------------------------------------------
MODE 5: Min/Max Characteristics (32-bit)
------------------------------------------------------------
Identify the characteristics of the Largest Positive Normalized Number.

What is the Sign bit?
Press `q` to exit.
>> 0
Correct.

What is the Exponent pattern (in binary)? 
(Hint: It cannot be all 1s, as that is reserved for INF/NaN)
Press `q` to exit.
>> 11111110
Correct.

What is the Fraction pattern (in binary)?
Press `q` to exit.
>> 11111111111111111111111
Correct.
```

---

## 6. Special Cases (NaN, INF, 0)

**Objective**: Quickly mapping patterns for IEEE 754 special encodings.

```text
------------------------------------------------------------
MODE 6: Special Cases (32-bit)
------------------------------------------------------------
Identify the required bit patterns for encoding: Negative Infinity (-INF)

Step 1: Sign Bit
Press `q` to exit.
>> 1
Correct.

Step 2: Exponent Pattern
Should the 8-bit exponent be all 0s, all 1s, or neither? (Type '0s', '1s', or 'N')
Press `q` to exit.
>> 1s
Correct. (All 1s: 11111111)

Step 3: Fraction Pattern
Should the 23-bit fraction be all 0s, or non-zero? (Type '0s' or 'NZ')
Press `q` to exit.
>> 0s
Correct. (All 0s)
```

---

## 7. Subnormals (Normalized vs Denormalized)

**Objective**: Test identifying subnormal representations and calculating their un-biased exponent (which is always 1 - bias).

```text
------------------------------------------------------------
MODE 7: Subnormals
------------------------------------------------------------
Analyze the sequence: 00000000011000000000000000000000

Is this value Normalized, Denormalized, or Special Case? (Type 'N', 'D', or 'S')
Press `q` to exit.
>> D
Correct. The exponent is all 0s and fraction is non-zero.

What is the implicit leading bit (1 or 0)?
Press `q` to exit.
>> 0
Correct. Denormalized values have an implicit leading 0.

What is the true (unbiased) exponent used for calculation?
(Hint: For denormals, true exp = 1 - bias)
Press `q` to exit.
>> -126
Correct.
```

---

## 8. Precision Impact

**Objective**: Observe how a single bit flip affects the floating-point value.

```text
------------------------------------------------------------
MODE 8: Precision Impact
------------------------------------------------------------
Original sequence: 01000000000000000000000000000000 (Value: 2.0)
Bit flipped at fraction LSB:
Modified seq:      01000000000000000000000000000001

Without calculating the exact value, did the value increase or decrease?
(Type '+' or '-')
Press `q` to exit.
>> +
Correct. The fraction increased and the number is positive.

What is the value of this 1 bit difference (the Machine Epsilon for this exponent)?
(Hint: It is 2^(true exp - 23))
Press `q` to exit.
>> 2^-22
Correct.
```

---

## 9. Rounding Modes

**Objective**: Convert numbers that cannot be exactly represented, applying a specific IEEE 754 rounding mode.

```text
------------------------------------------------------------
MODE 9: Rounding Modes
------------------------------------------------------------
Encode to 32-bit: 0.1
The binary fraction is infinitely repeating: 0.0001100110011...
Normalized: 1.100110011... x 2^-4

Fraction bits (first 25): 1001100110011001100110011...
Guard bit: 1
Round bit: 1
Sticky bit: 1 (Logical OR of all remaining bits)

Using Round to Nearest, Ties to Even (Default mode):
Should the 23rd bit of the fraction remain as-is (0) or round up (+1)?
(Type '0' to truncate, '+1' to round up)
Press `q` to exit.
>> +1
Correct. Guard bit is 1, and (Round | Sticky) is 1, so we round up.
```

---

## Quit Integration Handling

Typing `q` triggers a `UserQuitException` that immediately drops to the main menu without throwing standard python errors.

```text
What is the 8-bit Exponent sequence?
Press `q` to exit.
>> q

Exiting mode context...

============================================================
                  IEEE 754 TUTOR TERMINAL
============================================================
```
