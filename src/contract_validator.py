import yaml
from typing import Dict, List

class ContractValidator:
    """
    Validates code changes against an API contract defined in YAML (e.g., OpenAPI specification).
    
    This validator loads YAML contract files, indexes schema properties, and compares them
    against code changes detected by the AST parser. It identifies mismatches such as:
    - Fields deleted in code but still present in the contract (OUTDATED)
    - Fields added in code but missing from the contract (MISMATCH)
    
    Example:
        >>> validator = ContractValidator()
        >>> index = validator.load_and_index_contract('contract.yaml')
        >>> changes = [{'type': 'DELETE', 'field': 'email', 'model': 'User'}]
        >>> violations = validator.validate(changes, index)
    """
    
    def load_and_index_contract(self, yaml_path: str) -> Dict[str, List[str]]:
        """
        Loads a YAML contract file and creates an index of schemas and their properties.
        
        This method parses the YAML file and extracts field names from each schema
        definition, typically under 'components/schemas' in OpenAPI specifications.
        
        Args:
            yaml_path (str): Path to the YAML contract file.
            
        Returns:
            Dict[str, List[str]]: Dictionary mapping schema names to lists of field names.
                                 Example: {'UserSchema': ['id', 'name', 'email']}
        
        Raises:
            FileNotFoundError: If the YAML file doesn't exist.
            yaml.YAMLError: If the YAML file is malformed.
        
        Example:
            >>> validator = ContractValidator()
            >>> index = validator.load_and_index_contract('openapi.yaml')
            >>> print(index)
            {'UserSchema': ['id', 'first_name', 'email']}
        """
        print(f"\n📄 Loading API contract from: {yaml_path}")
        
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Error: Contract file not found at {yaml_path}")
            raise
        except yaml.YAMLError as e:
            print(f"❌ Error: Failed to parse YAML file - {e}")
            raise
        
        index: Dict[str, List[str]] = {}
        # Navigate to components -> schemas
        schemas = data.get('components', {}).get('schemas', {})
        
        if not schemas:
            print("⚠️  Warning: No schemas found in contract file")
        
        for schema_name, schema_details in schemas.items():
            properties = schema_details.get('properties', {})
            index[schema_name] = list(properties.keys())
            print(f"  📋 Schema '{schema_name}': {len(properties)} properties - {list(properties.keys())}")
            
        print(f"✅ Contract indexed: {len(index)} schema(s) loaded")
        return index

    def validate(self, changes_report: List[Dict[str, str]], contract_index: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """
        Compares the code change report against the contract index to find violations.
        
        This method checks each change (ADD/DELETE) against the contract to identify:
        - Deleted fields that still exist in the contract (OUTDATED)
        - Added fields that are missing from the contract (MISMATCH)
        
        Args:
            changes_report (List[Dict[str, str]]): List of changes from AST parser.
                Each change dict has keys: 'type', 'field', 'model'.
            contract_index (Dict[str, List[str]]): Schema index from load_and_index_contract().
            
        Returns:
            List[Dict[str, str]]: List of violations, where each violation is a dictionary
                                 with keys: 'type', 'field', 'schema', 'details'.
        
        Example:
            >>> changes = [{'type': 'DELETE', 'field': 'email', 'model': 'User'}]
            >>> index = {'UserSchema': ['id', 'email']}
            >>> violations = validator.validate(changes, index)
            >>> print(violations)
            [{'type': 'OUTDATED', 'field': 'email', 'schema': 'UserSchema',
              'details': 'Field deleted in code but remains in contract (UserSchema).'}]
        """
        print(f"\n🔍 Validating {len(changes_report)} change(s) against contract...")
        violations: List[Dict[str, str]] = []

        for change in changes_report:
            model_name = change['model']
            field_name = change['field']
            change_type = change['type']
            
            # Simple mapping: Model "User" -> Schema "UserSchema"
            schema_name = f"{model_name}Schema"
            
            if schema_name not in contract_index:
                print(f"  ⚠️  Warning: Schema '{schema_name}' not found in contract (skipping)")
                continue
                
            schema_fields = contract_index[schema_name]

            if change_type == 'DELETE':
                # Code deleted a field, check if it's still in the contract
                if field_name in schema_fields:
                    violation = {
                        'type': 'OUTDATED',
                        'field': field_name,
                        'schema': schema_name,
                        'details': f"Field deleted in code but remains in contract ({schema_name})."
                    }
                    violations.append(violation)
                    print(f"  🛑 VIOLATION: Field '{field_name}' deleted in code but still in contract")
            
            elif change_type == 'ADD':
                # Code added a field, check if it's in the contract
                if field_name not in schema_fields:
                    violation = {
                        'type': 'MISMATCH',
                        'field': field_name,
                        'schema': schema_name,
                        'details': f"Field added in code but missing from contract ({schema_name})."
                    }
                    violations.append(violation)
                    print(f"  🛑 VIOLATION: Field '{field_name}' added in code but missing from contract")
        
        print(f"\n📊 Validation complete: {len(violations)} violation(s) found")
        return violations
