
# /RfMRI/src/utils/logger.py

import logging
import logging.config
import os

def setup_logging(default_path='logging.conf', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration."""
    path = os.getenv(env_key, None) or default_path
    if os.path.exists(path):
        logging.config.fileConfig(path)
    else:
        logging.basicConfig(level=default_level)
        logger = logging.getLogger(__name__)
        logger.warning('Failed to load configuration file. Using default configs')

def get_logger(name):
    """Get a configured logger."""
    return logging.getLogger(name)
    