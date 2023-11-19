import logging
import sys,os
from datetime import datetime

LOG_DIR = 'logs'
LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
                    format="[%(asctime)s: %(name)s - %(levelname)s - %(filename)s : %(message)s]",
                    level=logging.INFO,
                    datefmt='%m-%d-%Y  %I:%M:%S %p'
                    )
