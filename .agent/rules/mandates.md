# Project Mandates

1. **Documentation Synchronization**: The root `README.md` file must be kept synchronized with changes to the project at all times. This includes keeping the features and descriptions, testing, and verification methods up to date.
2. **Traceability Compliance**: Forward and backward traceability for testing and maintenance must be strictly enforced by the Agent natively. This will be maintained through a json-based compliance matrix (`doc/compliance_matrix.json`). That compliance matrix must be updated for every change to the project, and that file itself must be created and validated manually by the Agent from the `doc/features.md` file, which acts as the source of truth for the project's features. This traceability process must be guaranteed by the Agent's reasoning, not automated via Python test scripts.
3. **Test Coverage**: 100% coverage for functional testing of all classes, methods, functions, and logic is a strict requirement.
4. **Formal Methods**: Formal methods validation must be employed using Z3 to verify both algorithm logic against the IEEE 754 standard and system code correctness via (Bounded) Model Checking, as specified in `doc/formal_methods.md`.
5. **UI/UX Prompt Standard**: The user must clearly see that they can quit with `q` from any mode at any time, or the program from the main menu. The standard prompt format in all areas is:
   ```text
   Press `q` to exit.
   >> 
   ```
6. **Binary String Presentation**: When displaying sequences of binary digits to the user for analysis, do not separate the fields (such as sign, exponent, fraction) with spaces. The binary strings must be contiguous to encourage active recall.
7. **Formal Methods Documentation Synchronization**: The `doc/bmc_tutorial.md` and `doc/formal_methods.md` files MUST be kept synchronized with the project's actual usage of Z3 formal methods and Bounded Model Checking. If a new class of formal verification proof is built (such as string bounding or precision bit-flipping), the tutorial documentation must be updated accordingly to teach it.
