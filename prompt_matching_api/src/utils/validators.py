from typing import Dict, Any, List, Optional
import re

class InputValidator:
    """Utility class for input validation functions."""
    
    @staticmethod
    def is_valid_string(value: Any, allow_empty: bool = False) -> bool:
        """
        Check if value is a valid string.
        
        Args:
            value: Value to check
            allow_empty: Whether to allow empty strings
            
        Returns:
            True if valid string, False otherwise
        """
        if not isinstance(value, str):
            return False
        
        if not allow_empty and not value.strip():
            return False
            
        return True
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        Check for missing required fields in data.
        
        Args:
            data: Data dictionary to validate
            required_fields: List of required field names
            
        Returns:
            List of missing field names
        """
        return [field for field in required_fields if field not in data]
    
    @staticmethod
    def validate_field_values(data: Dict[str, Any], field_constraints: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Validate field values against constraints.
        
        Args:
            data: Data dictionary to validate
            field_constraints: Dictionary mapping field names to allowed values
            
        Returns:
            Dictionary of field names to error messages for invalid fields
        """
        errors = {}
        
        for field, allowed_values in field_constraints.items():
            if field in data:
                if data[field] not in allowed_values:
                    errors[field] = f"Invalid value for {field}. Allowed values: {allowed_values}"
        
        return errors
    
    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input by trimming whitespace and enforcing length limits.
        
        Args:
            value: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            return str(value)
        
        # Trim whitespace
        sanitized = value.strip()
        
        # Enforce length limit if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def validate_json_structure(data: Dict[str, Any], expected_structure: Dict[str, type]) -> List[str]:
        """
        Validate that JSON data matches expected structure.
        
        Args:
            data: Data to validate
            expected_structure: Dictionary mapping field names to expected types
            
        Returns:
            List of validation errors
        """
        errors = []
        
        for field, expected_type in expected_structure.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], expected_type):
                errors.append(f"Field {field} must be of type {expected_type.__name__}")
        
        return errors

class PromptValidator:
    """Specialized validator for prompt matching requests."""
    
    # Define validation constants
    REQUIRED_FIELDS = ["situation", "level", "file_type", "data"]
    
    EXPECTED_STRUCTURE = {
        "situation": str,
        "level": str,
        "file_type": str,
        "data": str
    }
    
    MAX_DATA_LENGTH = 10000  # Maximum length for data field
    
    @classmethod
    def validate_prompt_request(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation for prompt matching requests.
        
        Args:
            data: Request data to validate
            
        Returns:
            Dictionary with validation results:
            {
                'is_valid': bool,
                'errors': List[str],
                'sanitized_data': Dict[str, Any]
            }
        """
        result = {
            'is_valid': True,
            'errors': [],
            'sanitized_data': {}
        }
        
        # Check JSON structure
        structure_errors = InputValidator.validate_json_structure(data, cls.EXPECTED_STRUCTURE)
        if structure_errors:
            result['errors'].extend(structure_errors)
            result['is_valid'] = False
            return result
        
        # Check for missing fields
        missing_fields = InputValidator.validate_required_fields(data, cls.REQUIRED_FIELDS)
        if missing_fields:
            result['errors'].append(f"Missing required fields: {', '.join(missing_fields)}")
            result['is_valid'] = False
            return result
        
        # Sanitize and validate individual fields
        sanitized_data = {}
        
        for field in cls.REQUIRED_FIELDS:
            if field == "data":
                # Data field can be empty but should be sanitized
                sanitized_data[field] = InputValidator.sanitize_string(
                    data[field], 
                    max_length=cls.MAX_DATA_LENGTH
                )
            else:
                # Other fields must not be empty
                if not InputValidator.is_valid_string(data[field], allow_empty=False):
                    result['errors'].append(f"Field {field} cannot be empty")
                    result['is_valid'] = False
                else:
                    sanitized_data[field] = InputValidator.sanitize_string(data[field])
        
        result['sanitized_data'] = sanitized_data
        
        return result