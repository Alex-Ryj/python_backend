import logging.config
import logging
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')
print('log file path', log_file_path)
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logging.debug('logging configured')


