import logging
import json
import sys
from typing import Any, Dict
from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """
    Structured JSON log formatter that includes correlation IDs and context safely.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "correlation_id"):
            log_obj["correlation_id"] = getattr(record, "correlation_id")

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


def setup_logging() -> logging.Logger:
    """
    Initializes application logging configuration.
    """
    logger = logging.getLogger("sih26100")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger


logger = setup_logging()
