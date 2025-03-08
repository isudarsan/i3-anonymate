import logging.config
import os
from pathlib import Path

import yaml


def setup_logging():
    """Reads logging configurations from .conf file, either default or via env variable LOGGING_CONF_PATH"""
    default_conf_path = Path(__file__).resolve().parent / "logging.conf"
    logging_conf_path = os.getenv("LOGGING_CONF_PATH", default_conf_path)
    logging.config.fileConfig(logging_conf_path, disable_existing_loggers=True)


def load_specific_recognizers_set(file_path: str | Path) -> set[str]:
    with open(file_path, "r") as file:
        specific_recognizers = yaml.safe_load(file)["specific_recognizers"] or []
        specific_recognizers = set(specific_recognizers)
    return specific_recognizers


SPECIFIC_RECOGNIZERS = load_specific_recognizers_set(
    Path(__file__).parent.resolve() / "recognizers" / "specific_recognizer_logging.yaml"
)
