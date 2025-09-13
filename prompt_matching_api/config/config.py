import os

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # API settings
    API_VERSION = "v1"
    API_TITLE = "Prompt Matching API"
    API_DESCRIPTION = "API for matching system prompts based on situation, level, and file type"
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/app.log'
    
    # Valid input options
    VALID_SITUATIONS = ["Commercial Auto", "General Liability", "Workers Compensation"]
    VALID_LEVELS = ["Structure", "Summarize"]
    VALID_FILE_TYPES = ["Medical Records", "Deposition", "Summons", "Summary Report"]
    
    # Prompt matching criteria
    PROMPT_CRITERIA = {
        "Prompt 1": {
            "situation": "Commercial Auto",
            "level": "Structure",
            "file_type": "Summary Report"
        },
        "Prompt 2": {
            "situation": "General Liability",
            "level": "Summarize",
            "file_type": "Deposition"
        },
        "Prompt 3": {
            "situation": "Commercial Auto",
            "level": "Summarize",
            "file_type": "Summons"
        },
        "Prompt 4": {
            "situation": "Workers Compensation",
            "level": "Structure",
            "file_type": "Medical Records"
        },
        "Prompt 5": {
            "situation": "Workers Compensation",
            "level": "Summarize",
            "file_type": "Summons"
        }
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}