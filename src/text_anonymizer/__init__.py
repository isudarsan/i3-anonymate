from text_anonymizer.logging_config import setup_logging
from text_anonymizer.text_anonymizer import TextAnonymizer
from text_anonymizer.utils import text_anonymizer_info

setup_logging()

__all__ = ["TextAnonymizer", "text_anonymizer_info"]
