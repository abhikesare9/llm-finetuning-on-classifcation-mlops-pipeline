import logging
import os

class SingletonLogger:
    _instance = None

    def __new__(cls, log_file='app.log', level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)

            # Configure the logger
            cls._instance.logger = logging.getLogger("SingletonLogger")
            cls._instance.logger.setLevel(level)

            # Create a file handler for logging to a file
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)

            # Create a console handler for logging to console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            # Create a formatter and set it for both handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add handlers to the logger
            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(console_handler)

        return cls._instance

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Usage Example
if __name__ == "__main__":
    logger = SingletonLogger('application.log', logging.DEBUG)
    
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
