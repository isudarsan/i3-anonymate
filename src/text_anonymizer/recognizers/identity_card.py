from typing import Optional

from presidio_analyzer import Pattern

from text_anonymizer import constants, triggerwords
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomIdentityCardRecognizer_CH(CustomPatternRecognizer):
    """
    Recognize valid swiss identity card number using regular expressions.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_IDENTITY_CARD]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SWITZERLAND]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_IDENTITY_CARD_CH = Pattern(
        name="pattern_passport_identity_card_ch",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<identity_card>[a-zA-Z\d]{1}\d{7,8})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_IDENTITY_CARD_CH]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_IDENTITY_CARD_DE_CH

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
            trigger_words=self.TRIGGER_WORDS,
            calling_recognizer=type(self).__name__,
        )


class CustomIdentityCardRecognizer_DE(CustomPatternRecognizer):
    """
    Recognize valid german identity card number using regular expressions.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_IDENTITY_CARD]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GERMANY]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_IDENTITY_CARD_DE = Pattern(
        name="pattern_passport_identity_card_de",
        regex=r"(?<![[A-ZÄÖÜa-zäöüß0-9]])(?P<IdentityCard>[LMNPRTVWXY]{1}[CFGHJKLMNPRTVWXYZ0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_IDENTITY_CARD_DE]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_IDENTITY_CARD_DE_DE

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
            trigger_words=self.TRIGGER_WORDS,
            calling_recognizer=type(self).__name__,
        )


class CustomIdentityCardRecognizer_ES(CustomPatternRecognizer):
    """
    Recognize valid spanish identity card number using regular expressions and result validation.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_IDENTITY_CARD]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SPAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_IDENTITY_CARD_ES = Pattern(
        name="pattern_identity_card_es:",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<DNI>[0-9]{8}[A-HJ-MP-TV-Z]{1})(?![A-ZÖÜÄ0-9,])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_IDENTITY_CARD_ES]

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
        )

    def validate_result(self, pattern_text: str) -> Optional[bool]:
        """
        Validate DNI
        """
        # Identify check digit.
        checkdigit = pattern_text[8]

        # Identify required string for calculation.
        requiredstr = int(pattern_text[:-1])

        # Modulo
        modulo = requiredstr % 23

        # Calculation
        if modulo == 0:
            isvalid = "T" == checkdigit
        elif modulo == 1:
            isvalid = "R" == checkdigit
        elif modulo == 2:
            isvalid = "W" == checkdigit
        elif modulo == 3:
            isvalid = "A" == checkdigit
        elif modulo == 4:
            isvalid = "G" == checkdigit
        elif modulo == 5:
            isvalid = "M" == checkdigit
        elif modulo == 6:
            isvalid = "Y" == checkdigit
        elif modulo == 7:
            isvalid = "F" == checkdigit
        elif modulo == 8:
            isvalid = "P" == checkdigit
        elif modulo == 9:
            isvalid = "D" == checkdigit
        elif modulo == 10:
            isvalid = "X" == checkdigit
        elif modulo == 11:
            isvalid = "B" == checkdigit
        elif modulo == 12:
            isvalid = "N" == checkdigit
        elif modulo == 13:
            isvalid = "J" == checkdigit
        elif modulo == 14:
            isvalid = "Z" == checkdigit
        elif modulo == 15:
            isvalid = "S" == checkdigit
        elif modulo == 16:
            isvalid = "Q" == checkdigit
        elif modulo == 17:
            isvalid = "V" == checkdigit
        elif modulo == 18:
            isvalid = "H" == checkdigit
        elif modulo == 19:
            isvalid = "L" == checkdigit
        elif modulo == 20:
            isvalid = "C" == checkdigit
        elif modulo == 21:
            isvalid = "K" == checkdigit
        elif modulo == 22:
            isvalid = "E" == checkdigit
        else:
            isvalid = False
        return isvalid


class CustomIdentityCardRecognizer_US(CustomPatternRecognizer):
    """
    Recognize US identity card numbers. (Only Social Security Number: SSN)

    https://www.ssa.gov/policy/docs/ssb/v45n11/v45n11p29.pdf
    https://www.ssa.gov/employer/stateweb.htm
    https://www.ssa.gov/history/ssn/geocard.html
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_IDENTITY_CARD]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_USA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_IDENTITY_CARD_US = Pattern(
        name="pattern_passport_identity_card_us",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<SSN>[0-7]{1}[0-9]{2}[- .]{0,1}[0-9]{2}[- .]{0,1}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9-])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_IDENTITY_CARD_US]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_IDENTITY_CARD_EN_US

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
            trigger_words=self.TRIGGER_WORDS,
            calling_recognizer=type(self).__name__,
        )
