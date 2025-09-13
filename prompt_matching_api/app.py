from flask import Flask
import logging
from src.controllers.prompt_controller import prompt_bp
from config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(prompt_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        from flask import jsonify
        return jsonify({
            "status": "healthy",
            "service": "Prompt Matching API"
        }), 200
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({
            "error": "Endpoint not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            "error": "Internal server error"
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("Starting Prompt Matching API...")
    print("Available endpoints:")
    print("  POST /api/match-prompt - Match prompts based on input criteria")
    print("  GET /health - Health check")
    print()
    print("Expected input format:")
    print("""
    {
        "situation": "Commercial Auto",
        "level": "Structure", 
        "file_type": "Summary Report",
        "data": ""
    }
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)