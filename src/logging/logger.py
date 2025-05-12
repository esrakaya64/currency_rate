import logging
from config.config import APP_CONFIG

def setup_logger():
    """Configure and return the application logger."""
    logging.basicConfig(
        level=getattr(logging, APP_CONFIG['log_level']),
        format=APP_CONFIG['log_format']
    )
    return logging.getLogger(__name__)

logger = setup_logger() 

