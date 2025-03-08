import logging
from typing import List, Set, Tuple

import regex as re
from presidio_analyzer import (
    AnalysisExplanation,
    LocalRecognizer,
    Pattern,
    RecognizerResult,
)
from spacy.tokens import Doc, Span

from text_anonymizer import constants, words_to_remove
from text_anonymizer.recognizer_base import (
    CustomPatternRecognizer,
    CustomRecognizerMixin,
    debug_logging,
)
from text_anonymizer.recognizers.person import person_denylist, person_regex

LOGGER = logging.getLogger(__name__)


class CustomPersonRecognizer_RuleEnhancedNER(LocalRecognizer, CustomRecognizerMixin):
    """
    Recognize PII entities using a pre-trained spaCy model with NER capabilities.
    NER results are cleansed in a post-processing step using rule based approaches.
    Since the spaCy pipeline is ran by the AnalyzerEngine, this recognizer extracts
    the entities from the NlpArtifacts and replaces their types to align with Presidio's.
    Then post-processing steps are applied to clean the results.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PERSON]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE - 0.1

    # Tuples containing own entity names and spaCy entity names,
    # for verifying that the right spaCy entity is used.
    PRESIDIO_TO_SPACY_MAPPINGS = [({"PERSON", "PER"}, {"PERSON", "PER"})]

    # Characters that are not allowed in valid PERSON span.
    PERSON_FORBIDDEN_CHARS_SPAN = r"[^a-zA-ZäöüÄÖÜß\.\-\–\s]"  # regex
    # Characters that are not allowed in valid PERSON tokens.
    PERSON_FORBIDDEN_CHARS_TOKEN = r"[^a-zA-ZäöüÄÖÜß\.\-\–]"  # regex
    # Set maximum number of tokens for a person span
    PERSON_MAX_TOKENS = 5

    # Denylist of lower-case words that will be excluded from NER result.
    # example of usage:
    #   original sentence: "Hallo Herr Schuhmacher"
    #   anonymization according to NER model: "Hallo ***"
    #   anonymization with denylisted word "herr": "Hallo Herr ***"
    PERSON_DENYLISTS = {
        constants.LANGUAGE_CODE_DE: person_denylist.DENYLIST_PERSON_DE,
        constants.LANGUAGE_CODE_EN: person_denylist.DENYLIST_PERSON_EN,
        constants.LANGUAGE_CODE_ES: person_denylist.DENYLIST_PERSON_ES,
    }

    def __init__(self, supported_language, supported_entities, supported_regions):
        LocalRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=self.validate_supported_entities(supported_entities=supported_entities),  # type: ignore
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)
        self.calling_recognizer = type(self).__name__

    def load(self) -> None:
        pass

    def analyze(self, text, entities, nlp_artifacts=None):
        results = []
        if not nlp_artifacts:
            LOGGER.error("No nlp_artefacts are provided.")
            raise ValueError("No nlp_artefacts are provided.")
        debugging_text = "entities nlp_artifacts for Person Recognizer: {}".format(nlp_artifacts.entities)
        debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
        debugging_text = "keywords nlp_artifacts for Person Recognizer: {}".format(nlp_artifacts.keywords)
        debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)

        for entity in entities:
            if entity not in self.supported_entities:
                continue
            debugging_text = "Process entity: {}".format(entity)
            debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)

            for ent in nlp_artifacts.entities:
                # Check whether NER label matches entity.
                if not self._is_match_with_entity(entity, ent.label_, self.PRESIDIO_TO_SPACY_MAPPINGS):
                    continue

                # Create RecognizerResults.
                some_results = self._create_results_from_entity_span(entity=entity, span=ent, doc=nlp_artifacts.tokens)

                if some_results:
                    debug_logging(
                        logger=LOGGER, calling_recognizer=self.calling_recognizer, matches=some_results, text=text
                    )
                    # Add RecognizerResults.
                    results.extend(some_results)

        return results

    def _create_results_from_entity_span(self, entity: str, span: Span, doc: Doc) -> List[RecognizerResult]:
        results = []

        spans = self._clean_entity_span(entity, span, doc)
        for span in spans:
            # Create RecognizerResult.
            textual_explanation = "Identified as {} by {}.".format(entity, self.__class__.__name__)
            explanation = self._build_spacy_explanation(self.SCORE, textual_explanation)
            result = RecognizerResult(entity, span.start_char, span.end_char, self.SCORE, explanation)
            results.append(result)
            debugging_text = "Created results: {}".format(results)
            debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)

        return results

    def _clean_entity_span(self, entity: str, span: Span, doc: Doc) -> List[Span]:
        spans = [span]

        if entity == constants.ENTITY_PERSON:
            return self._clean_person_span(span, doc)

        return spans

    def _clean_person_span(self, span: Span, doc: Doc) -> List[Span]:
        spans = []

        # Check for forbidden characters in span.
        match = re.search(self.PERSON_FORBIDDEN_CHARS_SPAN, span.text)
        if match:
            return spans

        # Reject too long spans.
        if len(span) > self.PERSON_MAX_TOKENS:
            return spans

        # Iterate over tokens of span.
        remove_token_idxs = []
        for i, token in enumerate(span):

            # Check for forbidden characters in token.
            match = re.search(self.PERSON_FORBIDDEN_CHARS_TOKEN, token.text)
            if match:
                remove_token_idxs.append(i)
                continue

            # Check for incorrect POS tag.
            if token.pos_ not in ["NOUN", "PROPN"]:
                remove_token_idxs.append(i)
                continue

            # Remove stop word tokens.
            if token.is_stop:
                remove_token_idxs.append(i)
                continue

            # Check for denylisted words.
            if token.text.lower() in self.PERSON_DENYLISTS[self.supported_language]:
                remove_token_idxs.append(i)
                continue

        # Create spans for approved tokens.
        is_inside_span = False
        add_span = False
        for i, token in enumerate(span):
            if i in remove_token_idxs:
                if is_inside_span:
                    is_inside_span = False
                    span_end_idx = span.start + i
                    add_span = True
            else:
                if not is_inside_span:
                    is_inside_span = True
                    span_start_idx = span.start + i
                if i == len(span) - 1:
                    span_end_idx = span.start + i + 1
                    add_span = True

            if add_span:
                spans.append(doc[span_start_idx:span_end_idx])  # type: ignore
                add_span = False

        return spans

    def _build_spacy_explanation(self, original_score: float, explanation: str) -> AnalysisExplanation:
        """
        Create explanation for why this result was detected.

        :param original_score: Score given by this recognizer
        :param explanation: Explanation string
        :return:
        """
        result = AnalysisExplanation(
            recognizer=self.__class__.__name__,
            original_score=original_score,
            textual_explanation=explanation,
        )
        return result

    @staticmethod
    def _is_match_with_entity(entity: str, label: str, entity_label_mappings: List[Tuple[Set, Set]]) -> bool:
        """
        Check whether label given by NER model matches entity.

        Args:
            entity (str): [description]
            label (str): [description]
            entity_label_mappings (List[Tuple[Set, Set]]): [description]

        Returns:
            bool: [description]
        """
        match_result = any(
            [entity in entity_group and label in label_group for entity_group, label_group in entity_label_mappings]
        )
        return match_result


class CustomPersonRecognizer_PatternBased(CustomPatternRecognizer):
    """
    Recognize PII entities with regex.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PERSON]
    POSSIBLE_REGIONS = constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    # Patterns for LANGUAGE_CODE_DE.
    PATTERN_DE_GREETING = Pattern(
        name="pattern_de_greeted_person",
        regex=person_regex.REGEX_DE_GREETED_PERSON,
        score=SCORE,
    )

    PATTERN_DE_GOODBYE = Pattern(
        name="pattern_de_goodbye_person",
        regex=person_regex.REGEX_DE_GOODBYE_PERSON,
        score=SCORE,
    )

    PATTERN_DE_FORM_EMAIL = Pattern(
        name="pattern_de_form_email_person",
        regex=person_regex.REGEX_DE_FORM_EMAIL_PERSON,
        score=SCORE,
    )

    PATTERN_DE_FORM_GENERAL = Pattern(
        name="pattern_de_form_general_person",
        regex=person_regex.REGEX_DE_FORM_GENERAL_PERSON,
        score=SCORE,
    )

    PATTERN_DE_TITLED = Pattern(
        name="pattern_de_titled_person",
        regex=person_regex.REGEX_DE_TITLED_PERSON,
        score=SCORE,
    )

    PATTERNS_DE = [
        PATTERN_DE_GREETING,
        PATTERN_DE_GOODBYE,
        PATTERN_DE_FORM_EMAIL,
        PATTERN_DE_FORM_GENERAL,
        PATTERN_DE_TITLED,
    ]

    # Patterns for LANGUAGE_CODE_EN.
    PATTERN_EN_GOODBYE = Pattern(
        name="pattern_en_goodbye_person",
        regex=person_regex.REGEX_EN_GOODBYE_PERSON,
        score=SCORE,
    )

    PATTERN_EN_TITLED = Pattern(
        name="pattern_en_titled_person",
        regex=person_regex.REGEX_EN_TITLED_PERSON,
        score=SCORE,
    )

    PATTERNS_EN = PATTERNS_DE + [PATTERN_EN_GOODBYE, PATTERN_EN_TITLED]

    # Patterns for LANGUAGE_CODE_ES.
    PATTERN_ES_GREETING = Pattern(
        name="pattern_es_greeted_person",
        regex=person_regex.REGEX_ES_GREETED_PERSON,
        score=SCORE,
    )

    PATTERN_ES_GOODBYE = Pattern(
        name="pattern_es_goodbye_person",
        regex=person_regex.REGEX_ES_GOODBYE_PERSON,
        score=SCORE,
    )

    PATTERN_ES_TITLED = Pattern(
        name="pattern_es_titled_person",
        regex=person_regex.REGEX_ES_TITLED_PERSON,
        score=SCORE,
    )

    PATTERNS_ES = PATTERNS_DE + [
        PATTERN_ES_GREETING,
        PATTERN_ES_GOODBYE,
        PATTERN_ES_TITLED,
    ]

    # Patterns by language.
    PATTERNS_MAP = {
        constants.LANGUAGE_CODE_DE: PATTERNS_DE,
        constants.LANGUAGE_CODE_EN: PATTERNS_EN,
        constants.LANGUAGE_CODE_ES: PATTERNS_ES,
    }

    # List of words to remove from pattern matches.
    WORDS_TO_REMOVE_FROM_MATCH = words_to_remove.WORDS_TO_REMOVE_PERSON

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
            patterns=self.PATTERNS_MAP[supported_language],
            supported_regions=supported_regions,
            words_to_remove_from_match=self.WORDS_TO_REMOVE_FROM_MATCH,
            calling_recognizer=type(self).__name__,
        )
