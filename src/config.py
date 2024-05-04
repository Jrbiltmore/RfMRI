
# /RfMRI/src/config.py

import os

class Config:
    """Base configuration settings."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///rfmri.db')
    LOGGER_NAME = 'rfmri_application'
    LOG_FILE = 'application.log'

class ProductionConfig(Config):
    """Production specific configuration."""
    DEBUG = False
    DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI', 'postgresql://user:password@localhost/prod_db')

class DevelopmentConfig(Config):
    """Development environment specific configuration."""
    DEBUG = True
    DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI', 'postgresql://user:password@localhost/dev_db')
    LOG_FILE = 'development.log'

class TestingConfig(Config):
    """Testing environment specific configuration."""
    TESTING = True
    DATABASE_URI = os.environ.get('TESTING_DATABASE_URI', 'sqlite:///:memory:')
    LOG_FILE = 'testing.log'

def get_config():
    """Retrieve the appropriate configuration class based on the environment."""
    env = os.getenv('FLASK_ENV', 'development').lower()
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
