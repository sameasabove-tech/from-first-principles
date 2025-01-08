import datetime as dt
import json
import logging
from typing import Any

from typing_extensions import override


LOG_RECORD_BUILTIN_ATTRS = [  # Attributes to include in log records
    "args",
    "asctime",
    "created",
    "exc_info",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
]


class MyJSONFormatter(logging.Formatter):
    """Custom JSON formatter for log records.

    Formats log records as JSON strings, including user-defined fields
    along with standard logging attributes.
    """

    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ) -> None:
        """Initializes the JSON formatter.

        Args:
            fmt_keys: A dictionary mapping format keys to log record
                      attributes. If None, defaults to an empty dictionary.
        """
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-formatted string representation of the log record.
        """
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)  # Convert to JSON string

    def _prepare_log_dict(self, record: logging.LogRecord) -> dict[str, Any]:
        """Prepares a dictionary representing the log record.

        Args:
            record: The log record to process.

        Returns:
            A dictionary containing log record attributes and their values.
        """
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.UTC
            ).isoformat(),
        }

        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {  # Apply formatting keys
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }

        message.update(always_fields)  # Add remaining fields

        return message


class DataFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().startswith("[data]")


class AutoStartQueueListener(logging.handlers.QueueListener):
    def __init__(self, queue, *handlers, respect_handler_level=False):
        super().__init__(queue, *handlers, respect_handler_level=respect_handler_level)
        # Start the listener immediately.
        self.start()
