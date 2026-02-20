# IEEE 754 Tutor

An interactive command-line application built entirely in Python designed to train developers, students, and engineers on the intricate bit-level mechanics of IEEE 754 floating-point numbers.

## Features and Educational Modes

Through nine specialized training modes, users learn to manually encode, decode, and interpret single and double-precision floats.

1. **32-bit (Single) Encoding:** Convert decimals to 32-bit binary representation.
2. **32-bit (Single) Decoding:** Convert 32-bit binary sequences back to decimal.
3. **64-bit (Double) Encoding:** Convert decimals to 64-bit binary representation.
4. **64-bit (Double) Decoding:** Convert 64-bit binary sequences back to decimal.
5. **Min/Max Value Characteristics:** Identify the defining characteristics of extreme values in 32-bit format.
6. **Special Cases:** Map patterns for NaNs, Infinity, and Zeros.
7. **Subnormals (Normalized vs Denormalized):** Identify subnormal representations and calculate their un-biased exponents.
8. **Precision Impact:** Observe how single bit flips at the least significant bit affect floating-point values via the Machine Epsilon.
9. **Rounding Modes:** Practice applying IEEE 754 default rounding methods (Round to Nearest, Ties to Even) to infinitely repeating fractions using Guard, Round, and Sticky bits.

**Continuous Learning:** All modes feature continuous loops, presenting a new problem immediately upon completion. Prompts are standardized as direct directives to encourage active recall of the IEEE 754 standard.

*Note: You can press `q` at any prompt to gracefully exit the current context and return to the main menu.*

## Project Structure

*   `main.py`: The root executable. Run via `python3 main.py` to start the interactive tutor.
*   `run_tests.py`: The root test runner. Run via `python3 run_tests.py` to execute the functional and formal proofs.
*   `src/ui.py`: Handles terminal clearing, display formatting, and user input validation (including the quit mechanism).
*   `src/engine.py`: Contains the core bitwise algebraic functions for encoding/decoding and representing Float32/Float64 formats.
*   `src/base_mode.py`: An abstract class providing the standard `run_round()` interface for all interactive modules.
*   `src/*_mode.py` and `src/precision_impact.py`: The individual modules containing the procedural questions and logic for the 9 distinct educational modes.

## Testing & Formal Verification

The project employs a rigorous, dual-layered testing methodology where functional correctness and formal safety are verified independently, ensuring extreme reliability.

1.  **Functional Unit Testing (100% Coverage):** We maintain a suite of **71 functional unit tests** in `tests/` that achieves **100% coverage** of all logic, function calls, and input validations across the entire project. These tests simulate user interactions and verify the tutor's behavior autonomously from the formal methods. Run via `python3 run_tests.py`.
2.  **Formal Verification (BMC):** Complementing the functional suite, we use **Bounded Model Checking** via the Z3 Theorem Prover. This suite of **11 formal verification models**, located in `tests/`, mathematically proves the integrity of the IEEE 754 conversion logic and system boundaries across the entire input space. Read `doc/formal_methods.md` for more details.

**Note:** Standard functional tests require no dependencies. Running the formal verification models requires the `z3-solver` module (`pip install z3-solver`). Total active test suite: **82 test cases**.

## AI Disclosure

**AI Contributions:**
The codebase, including the documentation, formal methods verification models and testing compliance matrices, were developed using Google Antigravity and Google Gemini 3.1 Pro using agentic workflows. All generated logic and architectures are verified using the dual functional and formal verification methods described above.

**Human Contributions:**
I designed the project, its requirements and scope, and supervised its development through numerous rounds of feedback and iteration.
