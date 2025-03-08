from presidio_analyzer import Pattern

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomMacAddressRecognizer(CustomPatternRecognizer):
    """
    Recognize MAC addresses using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_MAC_ADDRESS]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_MAC = Pattern(
        name="pattern_mac",
        regex=r"((?<![A-ZÄÖÜa-zäöüß0-9]|[-])(?P<HyphenSeparated>)([0-9A-Fa-f]{2}[-]){5}([0-9A-Fa-f]{2})(?![0-9a-fA-F]|[-]))|((?<![0-9a-fA-F]|[:])(?P<ColonSeparated>)([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})(?![0-9a-fA-F]|[:]))|((?<![0-9a-fA-F]|[.])(?P<DotSeparated>)([0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4})(?![A-ZÄÖÜa-zäöüß0-9]|[.][A-ZÄÖÜa-zäöüß0-9]))",
        score=SCORE,
    )
    PATTERNS = [PATTERN_MAC]

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        CustomPatternRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=supported_entities,
            patterns=self.PATTERNS,
            supported_regions=supported_regions,
            calling_recognizer=type(self).__name__,
        )
