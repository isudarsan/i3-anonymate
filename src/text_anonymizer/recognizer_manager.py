import logging
from types import ModuleType
from typing import List, Optional

from text_anonymizer import constants, recognizers, utils
from text_anonymizer.recognizer_base import CustomRecognizerMixin
from text_anonymizer.utils import debug_logging, log_and_reraise_exceptions

LOGGER = logging.getLogger(__name__)


class RecognizerManager:
    """The RecognizerManager knows about all recognizer classes and creates correct recognizer instances."""

    @log_and_reraise_exceptions(LOGGER)
    def __init__(
        self,
        languages: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
        regions: Optional[List[str]] = None,
        recognizer_package: ModuleType = recognizers,
    ):
        # Process arguments.
        languages, entities, regions = utils.process_key_arguments(
            languages=languages, entities=entities, regions=regions
        )

        # Load recognizer modules.
        utils.load_modules_from_package(package=recognizer_package)

        # Create recognizers.
        self.recognizers = self._create_recognizers(languages=languages, entities=entities, regions=regions)
        LOGGER.info("Created %s recognizers", len(self.recognizers))
        debugging_text = "Recognizers created: {}".format([recognizer.name for recognizer in self.recognizers])
        debug_logging(logger=LOGGER, log_message=debugging_text)

        # Set remaining instance variables.
        self.languages = languages
        self.entities = entities
        self.regions = regions

    @log_and_reraise_exceptions(LOGGER)
    def _create_recognizers(
        self, languages: List[str], entities: List[str], regions: List[str]
    ) -> List[CustomRecognizerMixin]:

        if not (languages and entities and regions):
            raise ValueError("Lists for languages, entities and regions cannot be empty.")

        # Get all recognizer classes.
        all_custom_recognizer_classes = utils.get_all_subclasses(CustomRecognizerMixin)
        recognizers = []

        # Select and create matching recognizers.
        for cls in all_custom_recognizer_classes:
            valid_languages = []
            valid_entities = []
            valid_regions = []

            if cls.get_possible_languages() is None:
                valid_languages = languages
            else:
                for language in cls.get_possible_languages():
                    if language in languages:
                        valid_languages.append(language)

            if cls.get_possible_entities() is None:
                valid_entities = entities
            else:
                for entity in cls.get_possible_entities():
                    if entity in entities:
                        valid_entities.append(entity)

            if cls.get_possible_regions() is None:
                valid_regions = regions
            elif cls.get_possible_regions() == constants.VALID_GLOBALLY:
                valid_regions = [constants.VALID_GLOBALLY]
            else:
                for region in cls.get_possible_regions():
                    if region in regions:
                        valid_regions.append(region)

            if valid_languages and valid_entities and valid_regions:
                for language in valid_languages:
                    # Instantiate one recognizer per region. This is crucial to be able to limit anonymization to specific regions. Presidio´s analyze methods do not offer regional support.
                    for region in valid_regions:
                        recognizers.append(
                            cls(
                                supported_language=language,
                                supported_entities=valid_entities,
                                supported_regions=[region],
                            )
                        )

        return recognizers

    def _is_language_supported_by_recognizer(self, recognizer: CustomRecognizerMixin, language) -> bool:
        is_supported = recognizer.get_supported_language() == language  # type: ignore
        return is_supported

    def _is_entities_supported_by_recognizer(self, recognizer: CustomRecognizerMixin, entities) -> bool:
        is_supported = any([entity in entities for entity in recognizer.get_supported_entities()])  # type: ignore
        return is_supported

    def _is_regions_supported_by_recognizer(self, recognizer: CustomRecognizerMixin, regions) -> bool:
        is_supported = any(
            [region in regions or region == constants.VALID_GLOBALLY for region in recognizer.get_supported_regions()]
        )
        return is_supported

    def select_recognizers(self, language: str, entities: List[str], regions: List[str]) -> List[CustomRecognizerMixin]:
        # Alternative: here we could filter for region only since Presidio´s analyze function filters for language and entity anyway.
        selected_recognizers = [
            recognizer
            for recognizer in self.recognizers
            if self._is_language_supported_by_recognizer(recognizer, language)
            and self._is_entities_supported_by_recognizer(recognizer, entities)
            and self._is_regions_supported_by_recognizer(recognizer, regions)
        ]
        return selected_recognizers
