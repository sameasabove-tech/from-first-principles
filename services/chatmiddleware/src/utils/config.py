import logging
import logging.config
import os
import uuid

import yaml


def setup_logging(path="src/config/logging_config.yaml"):
    """Configures the application's logging system based on a YAML configuration file.

    This function sets up logging for the application by reading a YAML configuration file,
    customizing log file names with unique session IDs (using `uuid`), and then applying the
    configuration using `logging.config.dictConfig()`.

    It also creates the log directory if it doesn't exist.

    Args:
        path (str, optional): The path to the YAML logging configuration file.
                              Defaults to 'src/config/logging_config.yaml'.

    Raises:
        FileNotFoundError: If the logging configuration file is not found.
        yaml.YAMLError: If there is an error parsing the YAML content.
        Exception: If any other error occurs during logging configuration.

    Returns:
        None
    """
    logger = logging.getLogger("main_logger")

    try:
        with open(path) as f:
            config = yaml.safe_load(f)

        # Extract directory from log file path and create if it doesn't exist
        log_file_path = config["handlers"]["logfile"]["filename"]
        log_dir = os.path.dirname(log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            logger.info(f"Log directory created: {log_dir}")

        session_id = str(uuid.uuid4())

        config["handlers"]["logfile"]["filename"] = config["handlers"]["logfile"][
            "filename"
        ].replace("session", f"session_{session_id}")

        logging.config.dictConfig(config)  # Configure logging
        logger.info(f"Logging configuration loaded from {path}")

    except FileNotFoundError:
        print(f"Error: Logging configuration file not found at {path}")
        raise  # Re-raise the exception to be handled by the caller
    except yaml.YAMLError as e:
        print(f"Error parsing logging configuration: {e}")
        raise  # Re-raise the exception to be handled by the caller
    except Exception as e:
        print(f"An unexpected error occurred during logging setup: {e}")
        raise  # Re-raise the exception to be handled by the caller
