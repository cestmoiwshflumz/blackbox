import logging
import logging.handlers
import yaml
import os
import re
import time


class CustomLogger(logging.Logger):
    _instances = {}

    @classmethod
    def get_logger(cls, name: str, config_path: str = "config/config.yaml"):
        if name not in cls._instances:
            cls._instances[name] = cls(name, config_path)
        return cls._instances[name]

    def __init__(self, name: str, config_path: str = "config/config.yaml"):
        super().__init__(name)
        self.config = self._load_config(config_path)
        self.setup_logger()

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            # Validate required config keys
            required_keys = [
                "logger.level",
                "logger.format",
                "logger.datefmt",
                "logger.filename",
                "logger.filemode",
                "logger.encoding",
                "logger.max_bytes",
                "logger.backup_count",
            ]
            for key in required_keys:
                if not self._nested_get(config, key.split(".")):
                    raise ValueError(f"Missing required config key: {key}")
            return config
        except Exception as e:
            raise RuntimeError(f"Failed to load or validate logging configuration: {e}")

    def _nested_get(self, d: dict, keys: list):
        for key in keys:
            d = d.get(key)
            if d is None:
                return None
        return d

    def setup_logger(self):
        log_level = self._get_config_value("logger.level")
        self.setLevel(getattr(logging, log_level))

        formatter = logging.Formatter(
            self._get_config_value("logger.format"),
            datefmt=self._get_config_value("logger.datefmt"),
        )

        log_filename = self._get_config_value("logger.filename")

        file_handler = logging.handlers.RotatingFileHandler(
            log_filename,
            mode=self._get_config_value("logger.filemode"),
            maxBytes=self._get_config_value("logger.max_bytes"),
            backupCount=self._get_config_value("logger.backup_count"),
            encoding=self._get_config_value("logger.encoding"),
        )

        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.addHandler(ch)

        self.debug_lvl = log_level == "DEBUG"

    def _get_config_value(self, key_path: str):
        keys = key_path.split(".")
        return self._nested_get(self.config, keys)

    def log(self, level: str, msg: str) -> None:
        """Logs a message with a specific level."""
        level_method = getattr(super(), level.lower(), None)
        if level_method:
            level_method(msg)
        else:
            super().info(f"Attempted to log with unrecognized level '{level}': {msg}")

    def debug(self, msg: str, *args, **kwargs) -> None:
        """Logs a debug message if the debug level is enabled."""
        if self.debug_lvl:
            super().debug(msg, *args, **kwargs)


# Example of using CustomLogger class
if __name__ == "__main__":
    logger: CustomLogger = CustomLogger.get_logger("blackbox")

    # Example logging calls
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
