import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from ast_parser import ASTParser
from contract_validator import ContractValidator

def run_verification():
    print("--- Starting Verification ---")
    
    # Paths
    base_dir = os.getcwd()
    file_before = os.path.join(base_dir, 'test_project', 'model_before.py')
    file_after = os.path.join(base_dir, 'test_project', 'model_after.py')
    contract_path = os.path.join(base_dir, 'test_project', 'contract.yaml')

    # Step 1: AST Parsing
    print("\n[1] Running AST Parser...")
    parser = ASTParser()
    changes = parser.compare_files(file_before, file_after)
    print(f"Changes Detected: {changes}")

    # Step 2: Contract Validation
    print("\n[2] Running Contract Validator...")
    validator = ContractValidator()
    index = validator.load_and_index_contract(contract_path)
    print(f"Contract Index: {index}")
    
    violations = validator.validate(changes, index)
    print(f"\nViolations Found: {violations}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_verification()
