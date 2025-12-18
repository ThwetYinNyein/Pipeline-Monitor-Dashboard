import os
from dotenv import load_dotenv
from typing import Tuple
from logging_setup import setup_logging

def init_pipeline(name: str, env_file: str = '.env', log_subdir: str | None = None) -> Tuple[object, str, str]:
    """Initialize pipeline environment and logging.

    Args:
        name: Name of the pipeline (used for logging)
        env_file: Name of the environment file (default: '.env')
        log_subdir: Optional subdirectory name for logs (default: pipeline name)

    Returns: 
        Tuple of (logger, base_dir, log_dir)
    """
    # Get the project root directory (where bootstrap.py is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load environment variables from project root
    env_path = os.path.join(base_dir, env_file)
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # Try to load from current directory as fallback
        load_dotenv(env_file)

    # Setup logging directory in project root/log/{pipeline_name}
    log_name = name
    log_dir = os.path.join(base_dir, 'log', log_subdir or log_name)
    logger = setup_logging(log_dir, log_name)
    
    logger.info(f"Pipeline '{name}' initialized")
    logger.info(f"Base directory: {base_dir}")
    logger.info(f"Log directory: {log_dir}")

    return logger, base_dir, log_dir
