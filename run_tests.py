import unittest
import sys
import os
import importlib

def check_z3():
    try:
        import z3
    except ImportError:
        print("Error: The 'z3-solver' module is not installed.", file=sys.stderr)
        print("This project requires Z3 for formal verification tests to run.", file=sys.stderr)
        print("Please resolve this dependency by running: pip install z3-solver", file=sys.stderr)
        sys.exit(1)

def main():
    check_z3()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Manually load modules since we cannot use __init__.py packages
    project_root = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(project_root, 'tests')
    
    sys.path.insert(0, project_root)
    sys.path.insert(0, tests_dir)
    
    for f in os.listdir(tests_dir):
        if f.startswith('test_') and f.endswith('.py'):
            mod_name = f[:-3]
            mod = importlib.import_module(mod_name)
            suite.addTests(loader.loadTestsFromModule(mod))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with 0 if successful, 1 if failures
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    main()
