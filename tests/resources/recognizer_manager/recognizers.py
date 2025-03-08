""" This module contains test recognizers for testing the recognizer_manager.
"""

from presidio_analyzer.entity_recognizer import EntityRecognizer

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomRecognizerMixin


class TestRecognizer_1(EntityRecognizer, CustomRecognizerMixin):
    POSSIBLE_LANGUAGES = [constants.LANGUAGE_CODE_DE]
    POSSIBLE_ENTITIES = [constants.ENTITY_ADDRESS]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GERMANY]

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        EntityRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=supported_entities,
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)


class TestRecognizer_2(EntityRecognizer, CustomRecognizerMixin):
    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PERSON]
    POSSIBLE_REGIONS = None

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        EntityRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=supported_entities,
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)


class TestRecognizer_3(EntityRecognizer, CustomRecognizerMixin):
    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PERSON]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GREAT_BRITAIN]

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        EntityRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=supported_entities,
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)


class TestRecognizer_4(EntityRecognizer, CustomRecognizerMixin):
    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_VIN]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        EntityRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=supported_entities,
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)
