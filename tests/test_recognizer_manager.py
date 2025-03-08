import pytest
from tests.resources import recognizer_manager as recognizer_manager_resources
from text_anonymizer import constants
from text_anonymizer.recognizer_manager import RecognizerManager
import os


class TestRecognizerManager:
    """Tests for the recognizer_manager module."""

    LANGUAGES = [constants.LANGUAGE_CODE_DE, constants.LANGUAGE_CODE_EN]
    ENTITIES = [constants.ENTITY_ADDRESS, constants.ENTITY_PERSON, constants.ENTITY_VIN]
    REGIONS = [constants.COUNTRY_CODE_GERMANY, constants.COUNTRY_CODE_GREAT_BRITAIN]

    @pytest.mark.skipif(os.getenv('FULL_TEST_RUN') == '1', reason='Skipped during full test run due to state dependency issues. Should be removed after refactoring I3-12961.')
    def test_RecognizerManager_initialization(self, recognizer_manager_unrestricted) -> None:

        # Test with non-restricting arguments.
        number_recognizers = len(recognizer_manager_unrestricted.recognizers)  # manager
        assert number_recognizers == 9, f"Registered Recognizers are: {recognizer_manager_unrestricted.recognizers}"

        # Test with restricting arguments.
        manager = RecognizerManager(
            languages=[constants.LANGUAGE_CODE_EN],
            entities=self.ENTITIES,
            regions=self.REGIONS,
            recognizer_package=recognizer_manager_resources,
        )
        number_recognizers = len(manager.recognizers)
        assert number_recognizers == 4

        # Test with even more restricting arguments.
        manager = RecognizerManager(
            languages=[constants.LANGUAGE_CODE_EN],
            entities=self.ENTITIES,
            regions=[constants.COUNTRY_CODE_GERMANY],
            recognizer_package=recognizer_manager_resources,
        )
        number_recognizers = len(manager.recognizers)
        assert number_recognizers == 2

    @pytest.mark.skipif(os.getenv('FULL_TEST_RUN') == '1', reason='Skipped during full test run due to state dependency issues. Should be removed after refactoring I3-12961.')
    def test_RecognizerManager_select_recognizers(self, recognizer_manager_unrestricted):

        manager = recognizer_manager_unrestricted

        # Test with restricting arguments.
        selected_recognizers_2 = recognizer_manager_unrestricted.select_recognizers(
            language=constants.LANGUAGE_CODE_EN,
            entities=self.ENTITIES,
            regions=self.REGIONS,
        )
        assert len(selected_recognizers_2) == 4, f"Selected Recognizers are: {selected_recognizers_2}"
        assert len(selected_recognizers_2) < len(manager.recognizers)

        # Test with restricting arguments II.
        selected_recognizers_1 = manager.select_recognizers(
            language=constants.LANGUAGE_CODE_DE,
            entities=self.ENTITIES,
            regions=self.REGIONS,
        )
        assert len(selected_recognizers_1) == 5
        assert len(selected_recognizers_1) < len(manager.recognizers)

        # Test with even more restricting arguments.
        selected_recognizers_2 = manager.select_recognizers(
            language=constants.LANGUAGE_CODE_EN,
            entities=self.ENTITIES,
            regions=[constants.COUNTRY_CODE_GERMANY],
        )
        assert len(selected_recognizers_2) == 2
        assert len(selected_recognizers_2) < len(manager.recognizers)
