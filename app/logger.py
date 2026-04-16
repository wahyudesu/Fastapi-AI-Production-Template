from loguru import logger

logger.add("app.log", rotation="10 MB")
