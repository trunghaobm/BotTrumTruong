import logging
import os

log_file = 'error_log.txt'

logging.basicConfig(
                filename='error_log.txt', 
                level=logging.ERROR, 
                format='%(asctime)s - %(levelname)s - %(message)s \n========================================================================\n')

def log_error(message):
    logging.error(msg=message)
