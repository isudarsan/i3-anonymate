import logging
from typing import Dict, List, Optional

from lingua import Language, LanguageDetector, LanguageDetectorBuilder
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

from text_anonymizer import constants
from text_anonymizer.exceptions import LanguageDetectionError
from text_anonymizer.recognizer_manager import RecognizerManager
from text_anonymizer.utils import (
    debug_logging,
    deprecated_method,
    log_and_reraise_exceptions,
    process_key_arguments,
)

LOGGER = logging.getLogger(__name__)


class TextAnonymizer:
    """
    Main class for text anonymization tasks.
    """

    @log_and_reraise_exceptions(LOGGER)
    def __init__(
        self,
        supported_languages: Optional[List[str]] = None,
        supported_entities: Optional[List[str]] = None,
        supported_regions: Optional[List[str]] = None,
    ):
        """Construct a text anonymizer instance.

        Args:
            supported_languages (Optional[List[str]], optional): The languages the text anonymizer should support.
                If set to 'None' all available languages are supported. Defaults to None.
            supported_entities (Optional[List[str]], optional): The entities/PIIs the text anonymizer should support.
                If set to 'None' all available entities are supported. Defaults to None.
            supported_regions (Optional[List[str]], optional): The regions of origin of the entities the
                text anonymizer should support. If set to 'None' all available regions are supported. Defaults to None.

        In order to get an overview of the available languages, entities and regions you can call the
        text_anonymizer_info function or consult the README.
        >>> from text_anonymizer import text_anonymizer_info
        >>> text_anonymizer_info()
        """
        # Process arguments.
        supported_languages, supported_entities, supported_regions = process_key_arguments(
            languages=supported_languages,
            entities=supported_entities,
            regions=supported_regions,
        )

        # Create NlpEngine.
        nlp_engine_configuration = self._update_nlp_configuration(supported_languages)
        provider = NlpEngineProvider(nlp_configuration=nlp_engine_configuration)
        nlp_engine = provider.create_engine()

        # Create AnalyzerEngine.
        self._presidio_analyzer = AnalyzerEngine(
            registry=None,  # type: ignore
            supported_languages=supported_languages,
            nlp_engine=nlp_engine,
        )

        # Create AnonymizerEngine.
        self._presidio_anonymizer = AnonymizerEngine()

        # Create recognizers.
        recognizer_manager = RecognizerManager(
            languages=supported_languages,
            entities=supported_entities,
            regions=supported_regions,
        )
        self._recognizer_manager = recognizer_manager

        # Set remaining instance variables.
        self._supported_languages = supported_languages
        self._supported_entities = supported_entities
        self._supported_regions = supported_regions
        self._nlp_engine = nlp_engine

    @staticmethod
    def _update_nlp_configuration(supported_languages: list[str]) -> dict[str, str | list[dict[str, str]]]:
        """Returns nlp-configuration that only contains language models that align with supported languages"""
        nlp_engine_configuration = constants.NLP_ENGINE_CONFIGURATION.copy()
        nlp_engine_configuration["models"] = [
            model_dict for model_dict in constants.NLP_MODELS_CONFIGS if model_dict["lang_code"] in supported_languages
        ]
        debugging_text = "Selected language models: {}".format(nlp_engine_configuration["models"])
        debug_logging(logger=LOGGER, log_message=debugging_text)
        return nlp_engine_configuration

    def _validate_method_arguments(
        self,
        technique: str,
        anonymize: bool = True,
        detect: bool = False,
        detect_language: bool = False,
        language: Optional[str] = None,
        entities: Optional[List[str]] = None,
        regions: Optional[List[str]] = None,
    ):
        """Process and validate the arguments given to the self.process method and self.anonymize method.

        Args:
            technique (str): The technique argument given to the self.process method.
            anonymize (bool): The anonymize argument given to the self.process method. Defaults to True.
            detect (bool): The detect argument given to the self.process method. Defaults to False.
            language (Optional[str], optional): The language argument given to the self.process method.
                Defaults to None.
            entities (Optional[List[str]], optional): The entities argument given to the self.process method.
                Defaults to None.
            regions (Optional[List[str]], optional): The regions argument given to the self.process method.
                Defaults to None.

        Returns:
            str, list[str], list[str], str: the valid language, entities, regions and technique
        """
        if detect_language is True and language is not None:
            raise ValueError(
                f"When detect_language is set to True, language needs to be set to None. '{language}' was given"
            )

        if detect_language is False and language is None:
            if len(self._supported_languages) == 1:
                language = self._supported_languages[0]
            else:
                error_template_unspecified_language = "This anonymizer supports more than one language. Please specify one of them explicitly. Supported: {}. Given: {}."
                raise ValueError(error_template_unspecified_language.format(self._supported_languages, language))
        if entities is None:
            entities = self._supported_entities
        if regions is None:
            regions = self._supported_regions

        error_template_not_supported = "This anonymizer supports the following {}: {}. Given: {}."

        if language not in self._supported_languages and detect_language is False:
            raise ValueError(error_template_not_supported.format("languages", self._supported_languages, language))
        if any([entity not in self._supported_entities for entity in entities]):
            raise ValueError(error_template_not_supported.format("entities", self._supported_entities, entities))
        if any([region not in self._supported_regions for region in regions]):
            raise ValueError(error_template_not_supported.format("regions", self._supported_regions, regions))

        error_template_not_available = "The following {} are available: {}. Given: {}."

        if technique not in constants.AVAILABLE_TECHNIQUES:
            raise ValueError(
                error_template_not_available.format(
                    "anonymization techniques",
                    constants.AVAILABLE_TECHNIQUES,
                    technique,
                )
            )

        error_template_no_tasks = (
            "No tasks specified. Please set one of the following arguments to True: {}. Given: {}."
        )

        if not (anonymize or detect):
            raise ValueError(error_template_no_tasks.format(["anonymize", "detect"], [anonymize, detect]))

        return language, entities, regions, technique

    @log_and_reraise_exceptions(LOGGER)
    def process(
        self,
        text: str,
        language: Optional[str] = None,
        detect_language: bool = False,
        entities: Optional[List[str]] = None,
        regions: Optional[List[str]] = None,
        anonymize: bool = True,
        anonymize_complete_vin: bool = False,
        technique: str = constants.TECHNIQUE_REPLACE,
        detect: bool = False,
    ) -> Dict:
        """Process a text. Main method for text anonymization tasks.

        Args:
            text (str): The text that should be processed.
            language (Optional[str], optional): The language of the text. If set to 'None' and this text anonymizer
                instance supports exactly one language, the text is assumed to be in that language. If set to 'None'
                and this text anonymizer instance supports more than one language, an exception is thrown. Defaults to
                None.
            detect_language (bool, optional): Determines whether language should be detected. Can only be set to True
                if language is None. If no supported language can be detected, an exception is raised. Defaults to False
            entities (Optional[List[str]], optional): The entities that should be found. If set to 'None' all supported
                entities of this text anonymizer instance are considered. Defaults to None.
            regions (Optional[List[str]], optional): The regions of origin of the entities that should be found. If set
                to 'None' all supported regions of this text anonymizer instance are considered. Defaults to None.
            anonymize (bool, optional): The flag that determines whether an anonymized version of the text is returned
                or not. If set to 'True' the result contains a key named 'text' and its value is the anonymized text.
                Defaults to True.
            anonymize_complete_vin (bool, optional): The flag that determines whether the whole VIN should be censored
                or the last 6 characters only. If set to 'True' the whole VIN is censored. Defaults to False.
            technique (str, optional): The anonymization technique used to censor the text. For a list of available
                anonymization techniques call the text_anonymizer_info function in module text_anonymizer or consult
                the README. Defaults to 'replace'.
            detect (bool, optional): The flag that determines whether a list of entities found in the text is returned
                or not. If set to 'True' the result contains a key named 'entities' and its value is a list of entities
                found in the text. Each entity is a dict containing the following keys: start, end, type. 'start' and
                'end' contain the start and end position of the entity. 'type' contains the type of the entity. If the
                list is empty, the text does not contain entities. Defaults to False.

        Returns:
            Dict: The result of the processing. The dictionary has the following schema and content,
                  when all relevant flags are enabled:
                    {
                        # A list of entities found in the text. This key is added to the dictionary,
                        if 'detect' is set to True.
                        'entities': List[
                            {
                                start: int,  # Start position of the entity in the original text.
                                end: int,  # End position of the entity in the original text.
                                type: str  # Type of the entity.
                            }
                        ],

                        # The anonymized version of the text. This key is added to the dictionary,
                        if 'anonymize' is set to True.
                        'text': str
                    }
        """
        # Process and validate arguments.
        language, entities, regions, technique = self._validate_method_arguments(
            technique=technique,
            anonymize=anonymize,
            detect=detect,
            detect_language=detect_language,
            language=language,
            entities=entities,
            regions=regions,
        )
        LOGGER.info("Pre processing text character count: %s", len(text))

        if detect_language:
            language = self._apply_language_detection(text)

        # Select recognizers.
        recognizers = self._recognizer_manager.select_recognizers(language=language, entities=entities, regions=regions)

        # Update AnalyzerEngine.
        self._presidio_analyzer.registry.recognizers = recognizers

        # Analyze text.
        analyzer_result = self._presidio_analyzer.analyze(text=text, language=language, entities=entities)

        # Prepare result dictionary.
        result = {}

        if detect:
            # Prepare found entities.
            found_entities = []
            for a_analyzer_result in analyzer_result:
                found_entity = {}
                found_entity["start"] = a_analyzer_result.start
                found_entity["end"] = a_analyzer_result.end
                found_entity["type"] = a_analyzer_result.entity_type
                found_entities.append(found_entity)

            # Add found entities to result dictionary.
            result["entities"] = found_entities
            LOGGER.info("Found %s entities", len(found_entities))

        if anonymize:
            # Adapt analyzer result for correct anonymization.
            if not anonymize_complete_vin:
                for a_analyzer_result in analyzer_result:
                    if a_analyzer_result.entity_type == constants.ENTITY_VIN:
                        new_start_idx = (
                            a_analyzer_result.end - 6
                            if a_analyzer_result.end - 6 >= a_analyzer_result.start
                            else a_analyzer_result.start
                        )
                        a_analyzer_result.start = new_start_idx

            # Set anonymization technique.
            anonymizer_operators = constants.PRESIDIO_ANONYMIZER_OPERATORS[technique]

            # Anonymize text.
            anonymizer_result = self._presidio_anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_result,
                operators=anonymizer_operators,
            )  # type: ignore
            anonymized_text = anonymizer_result.text

            # Add anonymized text to result dicitonary.
            result["text"] = anonymized_text
            LOGGER.info("Anonymized text characters count: %s", len(anonymized_text))

        return result

    @log_and_reraise_exceptions(LOGGER)
    def _apply_language_detection(self, text: str, language_detection_probability_distance: float = 0.2) -> str:
        """
        Detects whether the given text is in a supported language and returns its ISO 639-1 code.

        This method uses a language detection algorithm to determine if the provided text is written
        in one of the supported languages. If the language cannot be detected with high confidence or
        is not supported, a LanguageDetectionError is raised.

        Args:
            text (str): The text for which to detect the language.
            calculate_confidence_values (bool, optional): If True, calculates and stores the confidence
                values of detected languages. Default is False.
            language_detection_probability_distance (float, optional): The minimum relative distance
                for language detection to be considered confident. Default is 0.2.

        Returns:
            str: The ISO 639-1 code of the detected language if it is among the supported languages.

        Raises:
            LanguageDetectionError: If the language cannot be detected or is not supported.
        """
        language_detector = (
            LanguageDetectorBuilder.from_languages(*constants.LINGUA_LANGUAGES_FOR_DETECTION)
            .with_minimum_relative_distance(language_detection_probability_distance)
            .build()
        )
        detected_language_lingua = language_detector.detect_language_of(text)

        debugging_text = "Confidence levels of language detection: {}".format(
            self._create_confidence_values_dict(text, language_detector)
        )
        debug_logging(logger=LOGGER, log_message=debugging_text)

        if detected_language_lingua is None:
            raise LanguageDetectionError(
                "Language detection could not detect any supported language with high confidence."
            )

        detected_language_iso = detected_language_lingua.iso_code_639_1.name.lower()
        if detected_language_iso in self._supported_languages:
            LOGGER.info("Language '%s' detected", detected_language_iso)
            return detected_language_iso
        elif detected_language_iso in constants.AVAILABLE_LANGUAGES:
            raise LanguageDetectionError(
                f"Language '{detected_language_iso}' was detected but was not among "
                f"supported_languages of class. Supported languages: {self._supported_languages}"
            )
        else:
            raise LanguageDetectionError(
                f"Language '{detected_language_iso}' was detected but was not among "
                f"supported_languages of TextAnonymizer. Supported languages: {constants.AVAILABLE_LANGUAGES}"
            )

    @staticmethod
    def _create_confidence_values_dict(text: str, language_detector: LanguageDetector):
        detected_language_confidence_values = language_detector.compute_language_confidence_values(text)
        detected_language_confidence_values_dict = {
            confidence_value_object.language.iso_code_639_1.name: round(confidence_value_object.value, 4)
            for confidence_value_object in detected_language_confidence_values
        }
        return detected_language_confidence_values_dict

    @log_and_reraise_exceptions(LOGGER)
    @deprecated_method(alternative_method=process.__name__)
    def anonymize(
        self,
        text: str,
        language: Optional[str] = None,
        technique: str = constants.TECHNIQUE_REPLACE,
        entities: Optional[List[str]] = None,
        regions: Optional[List[str]] = None,
    ) -> str:
        """This method is deprecated and will be removed in later versions of this module. Use method process instead!

        Anonymize a text. Main method for text anonymization tasks.

        Args:
            text (str): The text that should be anonymized.
            language (Optional[str], optional): The language of the text. If set to 'None' and this text anonymizer
                instance supports exactly one language, the text is assumed to be in that language. If set to 'None'
                and this text anonymizer instance supports more than one language, an exception is thrown. Defaults to
                None.
            technique (str, optional): The anonymization technique used to censor the text. For a list of available
                anonymization techniques call the text_anonymizer_info function in module text_anonymizer or consult
                the README. Defaults to 'replace'.
            entities (Optional[List[str]], optional): The entities that should be anonymized. If set to 'None' all
                supported entities of this text anonymizer instance are considered. Defaults to None.
            regions (Optional[List[str]], optional): The regions of origin of the entities that should be anonymized.
                If set to 'None' all supported regions of this text anonyizer instance are considered. Defaults to None.

        Returns:
            str: anonymized text
        """
        # Process arguments.
        language, entities, regions, technique = self._validate_method_arguments(
            language=language, entities=entities, regions=regions, technique=technique
        )

        # Select recognizers.
        recognizers = self._recognizer_manager.select_recognizers(language=language, entities=entities, regions=regions)

        # Update AnalyzerEngine.
        self._presidio_analyzer.registry.recognizers = recognizers

        # Analyze text.
        analyzer_result = self._presidio_analyzer.analyze(text=text, language=language, entities=entities)

        # Set anonymization technique.
        anonymizer_operators = constants.PRESIDIO_ANONYMIZER_OPERATORS[technique]

        # Anonymize text.
        anonymizer_result = self._presidio_anonymizer.anonymize(
            text=text, analyzer_results=analyzer_result, operators=anonymizer_operators
        )  # type: ignore
        anonymized_text = anonymizer_result.text

        return anonymized_text
