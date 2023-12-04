from logs_utils import LoggerCreator
logger = LoggerCreator('server-logs').create_rotating_logger(log_name='server')
logger.info("Service is ready to use.")
logger.warning("wtf is wrong")
logger.error("Niggga.")
logger.critical("we got hacked.")