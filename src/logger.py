import logging
import os
from datetime import datetime

# Define the log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the log directory
log_path = os.path.join(os.getcwd(), "logs" , LOG_FILE)
os.makedirs(log_path, exist_ok=True)  # Ensure the directory exists

# Define thze full log file path
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info("Logging has started")
