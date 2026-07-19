import logging
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

# design the files 
Log_dir = "logs"
Log_file = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".log"
max_bytes = 10 * 1024 * 1024  # 10 MB
max_backup_count = 5

# lets create the log directory if it doesn't exist
project_root = Path(__file__).resolve().parents[2]
log_dir_path = project_root / Log_dir
log_dir_path.mkdir(parents=True, exist_ok=True)
log_file_path = log_dir_path / Log_file

def logggggg():
    """
        Configures logging with a rotating file handler and a console handler.
    """
    # create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # rember to add formating 
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # create a rotating file handler
    file_handler = RotatingFileHandler(str(log_file_path), maxBytes=max_bytes, backupCount=max_backup_count)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # create a stream handler for console output 
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter) # formating is done so the answe will be in a proper formate 

    # add the handlers to the logger 
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logggggg()
