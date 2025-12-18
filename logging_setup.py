import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

#Configuration
max_log_size = 10 * 1024 * 1024  # 10 MB
backup_count = 5

def setup_logging(log_dir, log_name, max_log_size=max_log_size, backup_count=backup_count):
    """
    Function to set up logging with a rotating file handler and console handler.
    
    Args:
        log_dir (str): Directory where log files will be stored.
        log_name (str): Base name for log files.
        max_log_size (int): Maximum log file size before rotating
        backup_count (int): Number of backup log files to keep.
        
    Returns:
        logger: Configured logger.
    """
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"{log_name}_{timestamp}.log")
    
    # Create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if called multiple times
    if logger.hasHandlers():
        return logger

    # Rotating file handler
    file_handler = RotatingFileHandler(log_filename, maxBytes=max_log_size, backupCount=backup_count, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)
    
    #To print stack trace both to file and consle
    logger.propagate = False
    return logger
