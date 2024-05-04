
# /RfMRI/config/production.py

import os

class ProductionConfig:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_production_secret_key')
    DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI', 'postgresql://produser:prodpassword@localhost/prod_rfmri')
    LOGGER_NAME = 'production_logger'
    LOG_FILE = '/var/log/rfmri/production.log'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Do not print SQL queries to stdout in production
    