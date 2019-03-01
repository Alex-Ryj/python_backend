import logging.config

logging.config.fileConfig('/log.conf', disable_existing_loggers=False)
logging.debug('logging configured')


