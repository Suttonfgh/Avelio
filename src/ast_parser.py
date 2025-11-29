import ast
from typing import List, Dict, Set

class FieldExtractor(ast.NodeVisitor):
    """
    Helper class to extract field names from class definitions in Python AST.
    
    This visitor traverses an Abstract Syntax Tree and identifies class definitions,
    extracting field names from annotated assignments (e.g., field: type) and regular
    assignments. It ignores methods and other non-field members.
    
    Attributes:
        classes (Dict[str, Set[str]]): Dictionary mapping class names to sets of field names.
    
    Example:
        >>> tree = ast.parse("class User:\\n    id: int\\n    name: str")
        >>> extractor = FieldExtractor()
        >>> extractor.visit(tree)
        >>> extractor.classes
        {'User': {'id', 'name'}}
    """
    def __init__(self) -> None:
        self.classes: Dict[str, Set[str]] = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visit a class definition node and extract field names.
        
        Args:
            node (ast.ClassDef): The class definition node to process.
        """
        fields: Set[str] = set()
        for item in node.body:
            # Handle annotated assignments (e.g., x: int)
            if isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    fields.add(item.target.id)
            # Handle regular assignments (e.g., x = 1)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.add(target.id)
        
        self.classes[node.name] = fields
        print(f"  📋 Found class '{node.name}' with {len(fields)} fields: {fields}")

class ASTParser:
    """
    Main class to parse and compare Python files for structural changes.
    
    This parser uses Python's built-in AST module to analyze code structure
    and detect field-level changes (additions and deletions) between two versions
    of a Python file. It focuses on class definitions and their fields.
    
    Example:
        >>> parser = ASTParser()
        >>> changes = parser.compare_files('model_v1.py', 'model_v2.py')
        >>> print(changes)
        [{'type': 'DELETE', 'field': 'old_field', 'model': 'User'},
         {'type': 'ADD', 'field': 'new_field', 'model': 'User'}]
    """
    
    def compare_files(self, file_before_path: str, file_after_path: str) -> List[Dict[str, str]]:
        """
        Compares two Python files and returns a list of field changes.
        
        This method parses both files into AST trees, extracts class fields,
        and compares them to identify additions and deletions.
        
        Args:
            file_before_path (str): Path to the original Python file.
            file_after_path (str): Path to the modified Python file.
            
        Returns:
            List[Dict[str, str]]: List of changes, where each change is a dictionary
                                 with keys 'type' (ADD/DELETE), 'field', and 'model'.
        
        Raises:
            FileNotFoundError: If either file doesn't exist.
            SyntaxError: If either file contains invalid Python syntax.
        """
        print(f"🔍 Parsing files for changes...")
        print(f"  Before: {file_before_path}")
        print(f"  After: {file_after_path}")
        
        try:
            fields_before = self._extract_fields(file_before_path)
            fields_after = self._extract_fields(file_after_path)
        except FileNotFoundError as e:
            print(f"❌ Error: File not found - {e}")
            raise
        except SyntaxError as e:
            print(f"❌ Error: Invalid Python syntax - {e}")
            raise

        changes: List[Dict[str, str]] = []

        # Compare fields for each class found in both files
        all_classes = set(fields_before.keys()) | set(fields_after.keys())
        print(f"\n📊 Analyzing {len(all_classes)} class(es)...")

        for model in all_classes:
            before_set = fields_before.get(model, set())
            after_set = fields_after.get(model, set())

            # Fields deleted
            deleted_fields = before_set - after_set
            for field in deleted_fields:
                changes.append({
                    'type': 'DELETE',
                    'field': field,
                    'model': model
                })
                print(f"  ❌ DELETE: {model}.{field}")

            # Fields added
            added_fields = after_set - before_set
            for field in added_fields:
                changes.append({
                    'type': 'ADD',
                    'field': field,
                    'model': model
                })
                print(f"  ✅ ADD: {model}.{field}")
        
        print(f"\n📝 Total changes detected: {len(changes)}")
        return changes

    def _extract_fields(self, file_path: str) -> Dict[str, Set[str]]:
        """
        Parses a Python file and extracts class fields.
        
        Args:
            file_path (str): Path to the Python file to parse.
            
        Returns:
            Dict[str, Set[str]]: Dictionary mapping class names to sets of field names.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            SyntaxError: If the file contains invalid Python syntax.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=file_path)
        extractor = FieldExtractor()
        extractor.visit(tree)
        return extractor.classes
