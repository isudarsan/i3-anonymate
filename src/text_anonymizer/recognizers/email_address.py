import logging
from typing import List, Optional

from presidio_analyzer import RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from presidio_analyzer.predefined_recognizers import EmailRecognizer

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomRecognizerMixin
from text_anonymizer.utils import debug_logging

LOGGER = logging.getLogger(__name__)


class CustomEmailAddressRecognizer(EmailRecognizer, CustomRecognizerMixin):
    """
    Recognize email addresses using Presidio´s pre-defined recognizer.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_EMAIL_ADDRESS]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    def __init__(self, supported_language, supported_entities, supported_regions):
        EmailRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entity=self.validate_supported_entities(supported_entities=supported_entities),  # type: ignore
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)

    def analyze(
        self,
        text: str,
        entities: List[str],
        nlp_artifacts: Optional[NlpArtifacts] = None,
        regex_flags: Optional[int] = None,
    ) -> List[RecognizerResult]:
        results = super().analyze(text, entities, nlp_artifacts, regex_flags)
        debug_logging(logger=LOGGER, calling_recognizer=type(self).__name__, matches=results, text=text)
        return results
