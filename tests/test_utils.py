import logging

import pytest

from text_anonymizer import utils

LOGGER = logging.getLogger(__name__)


class TestUtils:
    """Tests for the utils module."""

    def test_process_key_arguments(self):
        from text_anonymizer import constants

        # Test with input arguments that are not available in the current library.
        unknown_language = "unknown_language"
        unknown_entity = "unknown_entity"
        unknown_region = "unknown_region"

        throws_exception = False
        try:
            _ = utils.process_key_arguments(
                languages=[unknown_language],
                entities=[unknown_entity],
                regions=[unknown_region],
            )
        except:
            throws_exception = True
        finally:
            assert throws_exception

        # Test with input arguments that equal None.
        available_language = None
        available_entity = None
        available_region = None

        processed_languages, processed_entities, processed_regions = utils.process_key_arguments(
            languages=available_language,
            entities=available_entity,
            regions=available_region,
        )

        assert processed_languages == constants.AVAILABLE_LANGUAGES
        assert processed_entities == constants.AVAILABLE_ENTITIES
        assert processed_regions == constants.AVAILABLE_REGIONS

        # Test with input arguments that are valid.
        some_available_languages = [constants.LANGUAGE_CODE_DE]
        some_available_entities = [constants.ENTITY_PERSON]
        some_available_regions = [constants.COUNTRY_CODE_GREAT_BRITAIN]

        processed_languages, processed_entities, processed_regions = utils.process_key_arguments(
            languages=some_available_languages,
            entities=some_available_entities,
            regions=some_available_regions,
        )

        assert processed_languages == some_available_languages
        assert processed_entities == some_available_entities
        assert processed_regions == some_available_regions

    def test_load_modules_from_package(self):
        import sys

        from text_anonymizer import recognizers

        # Modules that should be imported with the method under test.
        module_names = [
            "text_anonymizer.recognizers.person",
            "text_anonymizer.recognizers.person.person_recognizer",
        ]

        # Test content of loaded modules after call to method under test.
        utils.load_modules_from_package(recognizers)
        for module_name in module_names:
            assert module_name in sys.modules

    @utils.log_and_reraise_exceptions(LOGGER)
    def raise_error_helper(self, parameter):
        raise ValueError(f"An error occured with parameter '{parameter}'")

    def test_log_and_reraise_exceptions_logging(self, caplog):
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError, match="An error occured with parameter 'param'"):
                self.raise_error_helper("param")
        assert "An error occured with parameter 'param'" in caplog.text

    def test_log_and_reraise_exceptions_reraising(self):
        with pytest.raises(ValueError, match="An error occured with parameter 'param'"):
            self.raise_error_helper("param")
