from typing import Dict, Any, Tuple
import logging
from config.config import Config

logger = logging.getLogger(__name__)

class PromptMatchingService:
    """Service class containing business logic for prompt matching."""
    
    @classmethod
    def validate_input_data(cls, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate input data structure and required fields.
        
        Args:
            data: Input dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Ensure data is a dictionary
        if not isinstance(data, dict):
            logger.warning(f"Invalid data type: expected dict, got {type(data).__name__}")
            return False, "Missing Data"
            
        required_fields = ["situation", "level", "file_type", "data"]
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.warning(f"Missing fields: {missing_fields}")
            return False, "Missing Data"
        
        # Check for empty or None values in required fields (except data which can be empty)
        for field in ["situation", "level", "file_type"]:
            field_value = data.get(field)
            
            # Check if field is None
            if field_value is None:
                logger.warning(f"None value for field: {field}")
                return False, "Missing Data"
            
            # Check if field is not a string
            if not isinstance(field_value, str):
                logger.warning(f"Invalid type for field {field}: expected str, got {type(field_value).__name__}")
                return False, "Missing Data"
            
            # Check if field is empty string
            if not field_value.strip():
                logger.warning(f"Empty or whitespace-only value for field: {field}")
                return False, "Missing Data"
        
        # Validate data field type (can be empty but must be string)
        data_field = data.get("data")
        if data_field is not None and not isinstance(data_field, str):
            logger.warning(f"Invalid type for data field: expected str, got {type(data_field).__name__}")
            return False, "Missing Data"
        
        return True, ""
    
    @classmethod
    def validate_field_values(cls, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that field values are within acceptable ranges.
        
        Args:
            data: Input dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        situation = data.get("situation")
        level = data.get("level")
        file_type = data.get("file_type")
        
        # Validate situation
        if situation not in Config.VALID_SITUATIONS:
            logger.warning(f"Invalid situation: {situation}")
            return False, "Invalid Prompt"
        
        # Validate level
        if level not in Config.VALID_LEVELS:
            logger.warning(f"Invalid level: {level}")
            return False, "Invalid Prompt"
        
        # Validate file_type
        if file_type not in Config.VALID_FILE_TYPES:
            logger.warning(f"Invalid file_type: {file_type}")
            return False, "Invalid Prompt"
        
        return True, ""
    
    @classmethod
    def match_prompt(cls, data: Dict[str, Any]) -> str:
        """
        Match input data to appropriate prompt.
        
        Args:
            data: Input dictionary containing situation, level, file_type, and data
            
        Returns:
            Matched prompt name
            
        Raises:
            ValueError: If no matching prompt is found
        """
        situation = data["situation"]
        level = data["level"]
        file_type = data["file_type"]
        
        # Search for matching prompt
        for prompt_name, criteria in Config.PROMPT_CRITERIA.items():
            if (criteria["situation"] == situation and 
                criteria["level"] == level and 
                criteria["file_type"] == file_type):
                
                logger.info(f"Matched {prompt_name} for input: {situation}, {level}, {file_type}")
                return prompt_name
        
        # No match found
        logger.warning(f"No matching prompt for: {situation}, {level}, {file_type}")
        raise ValueError("Invalid Prompt")
    
    @classmethod
    def process_request(cls, data: Dict[str, Any]) -> str:
        """
        Main processing method that validates input and returns matched prompt.
        
        Args:
            data: Input dictionary
            
        Returns:
            Matched prompt name
            
        Raises:
            ValueError: For various validation errors
        """
        # Validate input structure
        is_valid, error_msg = cls.validate_input_data(data)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Validate field values
        is_valid, error_msg = cls.validate_field_values(data)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Match prompt
        return cls.match_prompt(data)