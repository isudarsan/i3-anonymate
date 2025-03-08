from presidio_analyzer import Pattern

from text_anonymizer import constants, words_to_remove
from text_anonymizer.recognizer_base import CustomPatternRecognizer
from text_anonymizer.recognizers.address import (
    address_regex_at,
    address_regex_ch,
    address_regex_de,
    address_regex_es,
    address_regex_gb,
    address_regex_us,
)


class CustomAddressRecognizer_AT(CustomPatternRecognizer):
    """
    Recognize addresses from AT using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_AUSTRIA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    PATTERNS = [Pattern(name="address_AT", regex=address_regex_at.REGEX_AT_ADDRESS, score=SCORE)]

    WORDS_TO_REMOVE_FROM_MATCH = words_to_remove.WORDS_TO_REMOVE_ADDRESS_DE_AT

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
            words_to_remove_from_match=self.WORDS_TO_REMOVE_FROM_MATCH,
            calling_recognizer=type(self).__name__,
        )


class CustomAddressRecognizer_CH(CustomPatternRecognizer):
    """
    Recognize addresses from CH using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SWITZERLAND]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    PATTERNS = [Pattern(name="address_CH", regex=address_regex_ch.REGEX_CH_ADDRESS, score=SCORE)]

    # List of words to remove from pattern matches.
    WORDS_TO_REMOVE_FROM_MATCH = words_to_remove.WORDS_TO_REMOVE_ADDRESS_DE_CH

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
            words_to_remove_from_match=self.WORDS_TO_REMOVE_FROM_MATCH,
            calling_recognizer=type(self).__name__,
        )


class CustomAddressRecognizer_DE(CustomPatternRecognizer):
    """
    Recognize addresses from DE using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GERMANY]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    PATTERNS = [Pattern(name="address_DE", regex=address_regex_de.REGEX_DE_ADDRESS, score=SCORE)]

    # List of words to remove from pattern matches.
    WORDS_TO_REMOVE_FROM_MATCH = words_to_remove.WORDS_TO_REMOVE_ADDRESS_DE_DE

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
            words_to_remove_from_match=self.WORDS_TO_REMOVE_FROM_MATCH,
            calling_recognizer=type(self).__name__,
        )


class CustomAddressRecognizer_ES(CustomPatternRecognizer):
    """
    Recognize addresses from ES using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SPAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    PATTERNS = [Pattern(name="address_ES", regex=address_regex_es.REGEX_ES_ADDRESS, score=SCORE)]

    # List of words to remove from pattern matches.
    WORDS_TO_REMOVE_FROM_MATCH = words_to_remove.WORDS_TO_REMOVE_ADDRESS_ES_ES

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
            words_to_remove_from_match=self.WORDS_TO_REMOVE_FROM_MATCH,
            calling_recognizer=type(self).__name__,
        )


class CustomAddressRecognizer_GB(CustomPatternRecognizer):
    """
    Recognize addresses from GB using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GREAT_BRITAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    PATTERNS = [Pattern(name="address_GB", regex=address_regex_gb.REGEX_GB_ADDRESS, score=SCORE)]

    # List of words to remove from pattern matches.
    WORDS_TO_REMOVE_FROM_MATCH = words_to_remove.WORDS_TO_REMOVE_ADDRESS_EN_GB

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
            words_to_remove_from_match=self.WORDS_TO_REMOVE_FROM_MATCH,
            calling_recognizer=type(self).__name__,
        )


class CustomAddressRecognizer_US(CustomPatternRecognizer):
    """
    Recognize addresses from USA using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_USA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    PATTERNS = [Pattern(name="address_US", regex=address_regex_us.REGEX_US_ADDRESS, score=SCORE)]

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
