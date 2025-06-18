import logging
import sys

# Get logger
logger = logging.getLogger()

# Create formattter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)

# Create handlers
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Set formatter
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.handlers = [stream_handler, file_handler]

# set log level
logger.setLevel(logging.INFO)