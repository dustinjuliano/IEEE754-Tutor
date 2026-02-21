# IEEE 754 Tutor Features

1. Application Core
   1.1. Interactive command line terminal interface.
   1.2. Main menu allowing mode selection.
   1.3. Contextual exit mechanism (press 'q' to exit the current context and return to the previous, with the main menu resulting in quitting the program; 'q' instruction is briefed in prompts).
   1.4. Continuous educational loop (modes present problems consecutively until 'q' is pressed).

2. Educational Modes
   2.1. 32-bit (Single Precision) Encoding (from decimal/scientific to binary).
   2.2. 32-bit (Single Precision) Decoding (from binary to decimal).
   2.3. 64-bit (Double Precision) Encoding.
   2.4. 64-bit (Double Precision) Decoding.
   2.5. Min/Max Value Characteristics (identifying s, e, f for the 8 minimum/maximum standard values).
   2.6. Special Cases (recognizing ±NaN, ±INF, and ±0).
   2.7. Normalized vs. Denormalized Numbers (encoding/decoding subnormal values).
   2.8. Precision Impact (a proposed mode analyzing how single-bit flips impact the decoded value).
   2.9. Rounding Modes (a proposed mode practicing IEEE 754 rounding rules: to nearest, toward zero, toward +INF, toward -INF).

3. User Guidance
   3.1. Standardized interactive prompts (using direct directives like "Enter the..." to promote active recall).
   3.2. Step-by-step user guidance during encoding/decoding.
   3.3. Targeted error feedback: Single-sentence mathematical/structural explanations for incorrect answers to act as a virtual tutor.

4. Architecture & Compliance
   4.1. Extensible architecture to support new modes easily.
   4.2. Forward and backward compliance traceability mapping (Features <-> Code <-> Tests).
   4.3. Formal methods validation support.
