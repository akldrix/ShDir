import logging

from uvicorn.config import LOGGING_CONFIG

log_config = LOGGING_CONFIG.copy()


log_config["formatters"]["default"] = {
    "()": "uvicorn.logging.DefaultFormatter",
    "fmt": "%(message)s",
    "use_colors": True,
}

log_config["formatters"]["access"] = {
    "()": "uvicorn.logging.AccessFormatter",
    "fmt": '"%(request_line)s" %(status_code)s',
}

log_config["loggers"]["uvicorn.error"]["level"] = "WARNING"


log_config["loggers"]["uvicorn.access"]["level"] = "INFO"

logger = logging.getLogger("uvicorn")
