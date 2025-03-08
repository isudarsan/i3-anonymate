from typing import Optional

from luhn_validator import validate as luhn_validation
from presidio_analyzer import Pattern, pattern

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomImeiRecognizer(CustomPatternRecognizer):
    """
    Recognize IMEI codes using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_IMEI]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_IMEI = Pattern(
        name="pattern_imei",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<imei>[0-9]{15})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_IMEI]
    IMEI_LENGHT = 15

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

    def validate_result(self, pattern_text: str) -> Optional[bool]:
        """
        Validate the pattern logic e.g., by running checksum on a detected pattern.

        :param pattern_text: the text to validate.
        Only the part in text that was detected by the regex engine
        :return: A bool indicating whether the validation was successful.
        """
        is_valid = luhn_validation(number=pattern_text, length=self.IMEI_LENGHT)
        return is_valid
