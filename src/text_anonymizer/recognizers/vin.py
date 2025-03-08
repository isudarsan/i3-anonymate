from presidio_analyzer import Pattern

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomVinRecognizer(CustomPatternRecognizer):
    """
    Recognize VINs using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_VIN]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_VIN = Pattern(
        name="pattern_vin",
        # WMI is only allowed in UpperCase due to common use and to avoid false positives
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<WMI>[A-HJ-NPR-Z0-9]{2}[0-9A-HJ-NPR-Za-hj-npr-z]{1})[- ]{0,1}(?P<Attributes>[0-9A-HJ-NPR-Za-hj-npr-z]{6})[- ]{0,1}(?P<ModelYear>[0-9A-HJ-NPR-TV-Ya-hj-npr-tv-y]{1})[- ]{0,1}(?P<PlantCode>[0-9A-HJ-NPR-Za-hj-npr-z]{1})[- ]{0,1}(?P<SequentialNumber>[0-9]{6})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_VIN]

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
