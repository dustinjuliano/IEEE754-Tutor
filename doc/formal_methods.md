# Formal Methods Validation Proposal & Bounded Model Checking Tutorial

To meet the requirement for high-rigor formal methods validation using a Python module accessible via standard `pip`, we use the **Z3 Theorem Prover** via the `z3-solver` package.

## Introduction to Bounded Model Checking (BMC)
Bounded Model Checking is a powerful formal verification technique. Instead of relying purely on executing unit tests with sample input data (dynamic analysis), BMC creates mathematical models of a program's execution paths (static analysis).

### How BMC Works:
1.  **State Representation:** Program variables are translated into symbolic variables in a mathematical formula.
2.  **Path Unrolling:** Loops and recursive calls are "unrolled" up to a fixed bound *k* (hence "Bounded"). This transforms iterative behavior into straight-line formulas.
3.  **Property Assertion:** We assert specific properties or invariants that must hold true at various points or at the end of the execution (e.g., "no list index is out of bounds", "the output is always a valid IEEE 754 bit pattern").
4.  **SAT/SMT Solving:** An SMT solver (like Z3) attempts to find a combination of inputs that *violates* the assertion.
    *   If the solver outputs **UNSAT** (unsatisfiable), it means *no such violating inputs exist* within the bound. The code is mathematically proven correct up to that depth.
    *   If the solver outputs **SAT** (satisfiable), it provides a concrete counter-example: the exact inputs that trigger the bug.

### Why Z3?
Z3 natively supports Floating-Point Arithmetic (FPA) theory in compliance with the IEEE 754 standard. It provides `Float32` and `Float64` sorts that precisely evaluate special cases (NaNs, INFs, signed zeros, denormals) and rounding behaviors without the typical imprecision of native CPU floating-point operations.

---

## Comprehensive Validation Strategy

Our verification strategy goes beyond simple unit testing. It encompasses two critical phases for **100% source code coverage** via BMC, acting as a supplement to our 100% bidirectional traceability functional suite.

### Phase 1: Algorithmic Verification (Mathematical Correctness)
We use Z3's FPA theory to prove that our low-level encoding/decoding math produces identical bit representations and values as the state-of-the-art Z3 solver.
*   **Target:** `ieee754.engine` math functions.
*   **Method:** Assert that `CustomPythonLogic(s, e, f) == Z3_FP(s, e, f)` for all possible symbolic bitvectors `s`, `e`, and `f`.

### Phase 2: Complete Source Code Verification (Bounded Model Checking)
We will perform Bounded Model Checking on *every part* of the Python project to guarantee memory safety, bounds safety, and logic path correctness.

#### 1. Core Engine (`ieee754.engine`)
*   **What is checked:** Bit extraction, shifting, slicing, and arithmetic operations.
*   **BMC Approach:**
    *   Map incoming raw strings or floats to Z3 symbolic variables.
    *   Trace the execution path of slicing operations (e.g., `binary_str[1:9]`).
    *   **Assertions:** Prove that array indices never exceed bounds, that bitstring lengths are always strictly 32 or 64, and that bias arithmetic never underflows/overflows native Python capabilities unexpectedly.

#### 3. Educational Modes (`ieee754.modes.*`)
*   **What is checked:** The state machines and logic sequences driving each interactive mode.
*   **BMC Approach:**
    *   Model the sequence of steps and accepted input formats.
    *   **Assertions:** Prove that the state transitions correctly. If an invalid format is entered, prove that the error handling path is always taken. Prove that the "q to quit" exception is raised and handled precisely at the expected architectural boundary.

#### 4. UI Layer (`ieee754.ui`)
*   **What is checked:** Menu rendering, prompt display logic.
*   **BMC Approach:**
    *   Model the bounds of the menu list selections.
    *   **Assertions:** Prove that integer casting of user input correctly handles non-integer strings without crashing the main loop, returning to the prompt state reliably.

### Test Architecture & Integration
1.  **Dependency:** `z3-solver` added to standard requirements.
2.  **Directory:** `tests/formal/` contains the BMC assertion scripts. 
3.  **Process:** The test suite defines symbolic inputs, replicates the Python function's operational flow using Z3 operators, adds safety assertions, and asks Z3 to check for SAT (a bug) or UNSAT (proven safe).
4.  **Relation to Traceability:** This formal proof suite operates *in tandem* with the `doc/compliance_matrix.json` and 100% functional test suite, serving as mathematical proof of the assertions mapped in the matrix.
