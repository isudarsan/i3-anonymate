from presidio_analyzer import Pattern

from text_anonymizer import constants, triggerwords
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomPassportRecognizer_AT(CustomPatternRecognizer):
    """
    Recognize valid austrian passport number using regular expressions.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PASSPORT]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_AUSTRIA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_PASSPORT_AT = Pattern(
        name="pattern_passport_at",
        regex=r"(?<![A-ZÖÜÄ0-9,])(?P<Current>([A-Z]{1}[0-9]{7}))(?![A-ZÖÜÄ0-9,])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_PASSPORT_AT]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_PASSPORT_DE_AT

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


class CustomPassportRecognizer_CH(CustomPatternRecognizer):
    """
    Recognize valid swiss passport number using regular expressions.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PASSPORT]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SWITZERLAND]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_PASSPORT_CH = Pattern(
        name="pattern_passport_ch",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<current_since_2003>[a-zA-Z]\d{7})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_PASSPORT_CH]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_PASSPORT_DE_CH

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


class CustomPassportRecognizer_DE(CustomPatternRecognizer):
    """
    Recognize valid german passport number using regular expressions.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PASSPORT]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GERMANY]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_PASSPORT_DE = Pattern(
        name="pattern_passport_de",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<Passport>[CFGHJK]{1}[CFGHJKLMNPRTVWXYZ0-9]{8})(?![[A-ZÄÖÜa-zäöüß0-9]])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_PASSPORT_DE]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_PASSPORT_DE_DE

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


class CustomPassportRecognizer_ES(CustomPatternRecognizer):
    """
    Recognize valid spanish passport number using regular expressions.
    Temporary or children identity card or passport is not in scope.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PASSPORT]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SPAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_PASSPORT_ES = Pattern(
        name="pattern_passport_es",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<Currentsince2009>[A-Z]{3}[0-9]{6})(?![[A-ZÄÖÜa-zäöüß0-9]])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_PASSPORT_ES]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_PASSPORT_ES_ES

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


class CustomPassportRecognizer_GB(CustomPatternRecognizer):
    """
    Recognize valid uk passport number using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PASSPORT]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GREAT_BRITAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_PASSPORT_IDENTITY_CARD_GB = Pattern(
        name="pattern_passport_identity_card_gb",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<SequentialNumber>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_PASSPORT_IDENTITY_CARD_GB]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_PASSPORT_EN_GB

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


class CustomPassportRecognizer_US(CustomPatternRecognizer):
    """
    https://viatravelers.com/passport-travel-document-number/
    https://passportinfo.com/blog/what-is-my-passport-number/
    https://travel.state.gov/content/travel/en/passports/passport-help/next-generation-passport.html
    https://frascoprofiles.com/next-gen-us-passport-includes-a-letter-followed-by-8-digits/
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PASSPORT]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_USA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_PASSPORT_IDENTITY_CARD_US = Pattern(
        name="pattern_passport_identity_card_us",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<Currentsince2021>[A-Z]{1}[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9])|(?<![A-ZÄÖÜa-zäöüß0-9])(?P<SequentialNumber>[0-9]{6,9})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_PASSPORT_IDENTITY_CARD_US]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_PASSPORT_EN_US

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
