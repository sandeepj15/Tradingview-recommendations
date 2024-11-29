import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("FinancialDashboard")
    logger.setLevel(logging.DEBUG)  # You can set this to INFO, DEBUG, or ERROR

    # File handler for log file rotation
    handler = RotatingFileHandler(
        "financial_dashboard.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Stream handler for console logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console_handler)
    return logger
