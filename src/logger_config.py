import logging
import sys

def setup_logging():
    """Configures logging to both console and a file with UTF-8 support."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create a standard formatter
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # 1. File Handler - Explicitly set encoding to utf-8
    file_handler = logging.FileHandler("logs/etl_process.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 2. Stream Handler (Console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger