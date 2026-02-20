#!/usr/bin/env python3
import ast
import os
import glob
import sys
import argparse
from typing import List, Tuple

def get_all_ast_definitions(folder: str, exclude_init: bool = True) -> List[Tuple[str, str, str]]:
    """
    Recursively scans a target directory for Python files and uses the Abstract Syntax Tree (AST)
    to extract every class, method, and function definition, returning them as a standardized tracking list.
    
    Args:
        folder (str): The target directory to scan (e.g., 'src').
        exclude_init (bool): Whether to ignore `__init__.py` files. Default True.
        
    Returns:
        List[Tuple[str, str, str]]: A list of tuples containing (module_name, definition_type, definition_name)
    """
    definitions = []
    py_files = glob.glob(os.path.join(folder, "**", "*.py"), recursive=True)
    
    for py_file in py_files:
        if exclude_init and os.path.basename(py_file) == "__init__.py":
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except Exception as e:
            print(f"Error parsing {py_file}: {e}", file=sys.stderr)
            continue
            
        # Determine the modular path relative to the target folder
        rel_path = os.path.relpath(py_file, folder)
        module_name = rel_path.replace(os.sep, ".").replace(".py", "")
        
        class DefinitionVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_class = None
                
            def visit_ClassDef(self, node):
                definitions.append((module_name, "class", node.name))
                old_class = self.current_class
                self.current_class = node.name
                self.generic_visit(node)
                self.current_class = old_class
                
            def visit_FunctionDef(self, node):
                if self.current_class:
                    definitions.append((module_name, "method", f"{self.current_class}.{node.name}"))
                else:
                    definitions.append((module_name, "function", node.name))
                self.generic_visit(node)
                
            def visit_AsyncFunctionDef(self, node):
                self.visit_FunctionDef(node)

        visitor = DefinitionVisitor()
        visitor.visit(tree)
        
    return definitions

def main():
    parser = argparse.ArgumentParser(description="Modular AST definition extractor for Python projects.")
    parser.add_argument("directory", help="The root directory to analyze (e.g. 'src/' or '.')")
    parser.add_argument("--include-init", action="store_true", help="Include __init__.py files in output")
    parser.add_argument("--format", choices=['text', 'csv'], default='text', help="Output format")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.", file=sys.stderr)
        sys.exit(1)
        
    defs = get_all_ast_definitions(args.directory, exclude_init=not args.include_init)
    
    if args.format == 'csv':
        print("Module,Type,Name")
        for module, dtype, name in sorted(defs):
            print(f"{module},{dtype},{name}")
    else:
        print(f"{'Module':<30} | {'Type':<10} | {'Definition Name'}")
        print("-" * 80)
        for module, dtype, name in sorted(defs):
            print(f"{module:<30} | {dtype:<10} | {name}")

if __name__ == "__main__":
    main()
