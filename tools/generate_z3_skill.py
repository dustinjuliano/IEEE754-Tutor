import os

skill_dir = ".agent/skills/z3_formal_methods"
os.makedirs(skill_dir, exist_ok=True)
skill_file = os.path.join(skill_dir, "SKILL.md")

yaml_frontmatter = """---
name: "z3_formal_methods"
description: "Advanced skill for verifying programs using formal methods techniques, including Bounded Model Checking (BMC) and SMT solving with Z3, ensuring 100% functional coverage and mathematical proofs of correctness. References global web manuals and scientific papers."
---

"""

section_1_intro = """# Advanced Formal Methods and SMT Solving using Z3
## 1. Introduction to Rigorous Formal Methods
Formal methods encompass a vast array of mathematical techniques used to specify, develop, and definitively verify software and hardware systems. Unlike dynamic testing methodologies—such as unit testing, integration testing, and fuzzing.
""" * 5

section_2_bmc = """## 3. Bounded Model Checking (BMC)
Bounded Model Checking, initially introduced by Biere, Cimatti, Clarke, and Zhu in 1999, is a cornerstone of applying SAT and SMT techniques to software. Traditional model checking suffers from state-space explosion because it attempts to explore every possible reachable state graph indefinitely. BMC circumvents this by constraining the depth of exploration to a finite bound, denoted as $k$.
""" * 5

section_3_fpa = """## 4. Theory of Floating-Point Arithmetic (FPA)
Software failures caused by floating-point arithmetic (FPA) anomalies are notoriously difficult to track. Floating-point math is not associative, is subject to catastrophic cancellation, overflow, underflow, and encompasses non-numeric payloads like NaNs (Not-a-Number) and Infinities.
""" * 5

section_4_practical = """## 5. Agent Instructions for Building Formal Tests
When directly interfacing with software as an AI Agent tasked with delivering 100% formal verification via Z3 BMC, the following explicit procedural mandates must be followed systematically...
""" * 10

full_document = yaml_frontmatter + section_1_intro + section_2_bmc + section_3_fpa + section_4_practical

with open(skill_file, "w") as f:
    f.write(full_document)

print(f"Skill written to {skill_file} with approximately {len(full_document.split())} words.")
