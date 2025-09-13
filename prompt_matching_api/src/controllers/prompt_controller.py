from flask import Blueprint, request, jsonify
import logging
from src.services.prompt_service import PromptMatchingService

logger = logging.getLogger(__name__)

# Create blueprint
prompt_bp = Blueprint('prompt', __name__)

class PromptController:
    """Controller class handling HTTP requests and responses."""
    
    @staticmethod
    def handle_prompt_matching():
        """Handle POST request for prompt matching."""
        try:
            # Check if request contains JSON
            if not request.is_json:
                logger.warning("Request without JSON content-type received")
                return jsonify({
                    "error": "Content-Type must be application/json"
                }), 400
            
            # Get JSON data from request with error handling
            try:
                request_data = request.get_json(force=True)
            except Exception as json_error:
                logger.warning(f"Invalid JSON received: {str(json_error)}")
                return jsonify({
                    "error": "Invalid JSON format"
                }), 400
            
            # Handle case where JSON is None or empty
            if request_data is None:
                logger.warning("Empty JSON request received")
                return jsonify({
                    "error": "Missing Data"
                }), 400
            
            # Check if request_data is not a dictionary
            if not isinstance(request_data, dict):
                logger.warning(f"Invalid JSON structure - expected object, got {type(request_data).__name__}")
                return jsonify({
                    "error": "Invalid JSON structure - expected JSON object"
                }), 400
            
            logger.info(f"Processing request: {request_data}")
            
            # Process request through service layer
            matched_prompt = PromptMatchingService.process_request(request_data)
            
            # Return success response
            response = {
                "matched_prompt": matched_prompt,
                "status": "success"
            }
            logger.info(f"Request successful: {response}")
            return jsonify(response), 200
            
        except ValueError as e:
            # Handle business logic errors
            error_message = str(e)
            
            logger.warning(f"Validation error: {error_message}")
            
            if error_message == "Missing Data":
                return jsonify({
                    "error": "Missing Data"
                }), 400
            elif error_message == "Invalid Prompt":
                return jsonify({
                    "error": "Invalid Prompt"
                }), 400
            else:
                return jsonify({
                    "error": "Invalid Prompt"
                }), 400
        
        except TypeError as e:
            # Handle type errors (like trying to access dict methods on non-dict)
            logger.warning(f"Type error: {str(e)}")
            return jsonify({
                "error": "Invalid data format"
            }), 400
                
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({
                "error": "Internal server error"
            }), 500


# Route definitions
@prompt_bp.route('/match-prompt', methods=['POST'])
def match_prompt():
    """API endpoint for prompt matching."""
    return PromptController.handle_prompt_matching()

@prompt_bp.route('/match-prompt', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def method_not_allowed():
    """Handle unsupported HTTP methods."""
    logger.warning(f"Unsupported method {request.method} attempted on /match-prompt")
    return jsonify({
        "error": "Method not allowed. Only POST requests are supported."
    }), 405