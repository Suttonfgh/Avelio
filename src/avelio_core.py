"""
Avelio Core - Architectural Guard for AI-Generated Code

This is the main entry point for the Avelio MVP, an architectural sentinel that
analyzes code changes (typically from AI agents) and validates them against API
contracts to prevent integration failures.

Usage:
    python src/avelio_core.py
    
The script will:
1. Compare Python model files (before/after changes)
2. Load and index the API contract (YAML)
3. Validate changes against the contract
4. Report violations in CI/CD-friendly Markdown format
5. Exit with code 1 if violations are found (to fail builds)

Author: Avelio Development Team
Version: MVP 1.0
"""

import sys
import os
from typing import List, Dict

# Ensure we can import from the same directory when running as a script
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ast_parser import ASTParser
    from contract_validator import ContractValidator
else:
    from .ast_parser import ASTParser
    from .contract_validator import ContractValidator


def main() -> None:
    """
    Main orchestrator for the Avelio architectural validation pipeline.
    
    This function coordinates the three-stage process:
    1. AST Parsing: Detect structural changes in Python code
    2. Contract Loading: Index API contract schemas
    3. Validation: Cross-reference changes against contract
    
    Exit Codes:
        0: Success - No violations found
        1: Failure - Violations detected or execution error
    """
    print("=" * 70)
    print("🛡️  AVELIO - Architectural Guard for AI-Generated Code")
    print("=" * 70)
    print("Version: MVP 1.0")
    print("Mission: Preventing API Contract Violations in AI-Assisted Development")
    print("=" * 70)
    
    # Hard-coded paths relative to this file for robustness
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    FILE_BEFORE = os.path.join(base_dir, 'test_project', 'model_before.py')
    FILE_AFTER = os.path.join(base_dir, 'test_project', 'model_after.py')
    CONTRACT_FILE = os.path.join(base_dir, 'test_project', 'contract.yaml')
    
    print(f"\n📂 Configuration:")
    print(f"   Base Directory: {base_dir}")
    print(f"   Before Model: {os.path.basename(FILE_BEFORE)}")
    print(f"   After Model: {os.path.basename(FILE_AFTER)}")
    print(f"   Contract: {os.path.basename(CONTRACT_FILE)}")

    # Initialize components
    parser = ASTParser()
    validator = ContractValidator()

    try:
        # Stage 1: Parse and compare files
        print("\n" + "=" * 70)
        print("STAGE 1: AST PARSING & DIFF ANALYSIS")
        print("=" * 70)
        changes_report = parser.compare_files(FILE_BEFORE, FILE_AFTER)
        
        # Stage 2: Load contract
        print("\n" + "=" * 70)
        print("STAGE 2: CONTRACT LOADING & INDEXING")
        print("=" * 70)
        contract_index = validator.load_and_index_contract(CONTRACT_FILE)
        
        # Stage 3: Validate
        print("\n" + "=" * 70)
        print("STAGE 3: CONTRACT VALIDATION")
        print("=" * 70)
        violations = validator.validate(changes_report, contract_index)
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Could not find file - {e}")
        print("Please ensure all test files exist in the test_project directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: Unexpected error during execution - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Generate final report
    print("\n" + "=" * 70)
    print("FINAL REPORT")
    print("=" * 70)
    
    if not violations:
        print("\n## ✅ AVELIO CHECK: API Contract is VALID\n")
        print("No architectural violations detected.")
        print("All code changes are properly reflected in the API contract.")
        print("\n" + "=" * 70)
        sys.exit(0)
    else:
        # Markdown-formatted output for CI/CD integration
        print("\n## 🛑 Avelio Architectural Violations Detected\n")
        print(f"**Total Violations:** {len(violations)}\n")
        print("**Details:**\n")
        
        for i, v in enumerate(violations, 1):
            print(f"- **Violation {i}:** Field `{v['field']}` [{v['type']}]")
            print(f"  - **Schema:** {v['schema']}")
            print(f"  - **Issue:** {v['details']}")
            print()
        
        print("**Recommended Actions:**")
        print("- Review the changes to ensure API contract consistency")
        print("- Update the contract.yaml file to match code changes")
        print("- Re-run Avelio after fixing the violations")
        print("\n" + "=" * 70)
        print("❌ BUILD FAILED - Avelio detected contract violations")
        print("=" * 70 + "\n")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
