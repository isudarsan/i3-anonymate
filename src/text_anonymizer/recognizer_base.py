import logging
from typing import List, Optional, Tuple, Union

import regex as re
from presidio_analyzer import EntityRecognizer, PatternRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts

from text_anonymizer.utils import debug_logging

LOGGER = logging.getLogger(__name__)


class CustomRecognizerMixin:
    """Mixin class for recognizers of this library. Do not instantiate it directly.

    When implementing a recognizer for this library
    1) derive a child class from one of Presidio's recognizer base classes and from this class.
    2) add the prefix 'Custom' to the name of the derived class. This states that it is not a pre-defined recognizer of the Presidio Analyzer library.
    3) overwrite the class variables of this class inside the derived class. Otherwise the derived class signals that it does not support any language, entity and region to the recognizer manager. Hence the derived class would never be used as a recognizer.
    4) call the constructor of this class inside the derived class to initialize the instance variables. Otherwise the recognizer is not aware of its supported regions and the recognizer manager cannot validate its supported region.

    """

    # Overwrite these class variables in a derived class.
    # These variables signal which languages, entities and regions the recognizer can support and can be instantiated with.
    # '[]' -> the recognizer does not support any language, entity or region.
    # 'None' -> the recognizer is able to support any language, entity or region currently available as part of the library and can be instantiated with any combination of these values.
    # 'POSSIBLE_REGIONS = constants.VALID_GLOBALLY' -> the entities the recognizer supports are valid globally and a regional distinction is not desired.
    # 'list[str]' -> any other value has to be a list of strings where each string stands for a language, entity or region the recognizer is able to support and can be instantiated with.
    POSSIBLE_LANGUAGES = []
    POSSIBLE_ENTITIES = []
    POSSIBLE_REGIONS = []

    def __init__(self, supported_regions: List[str]):
        self.supported_regions = supported_regions

    def get_supported_regions(self) -> List[str]:
        return self.supported_regions

    @classmethod
    def get_possible_languages(cls) -> Union[List[str], None]:
        return cls.POSSIBLE_LANGUAGES

    @classmethod
    def get_possible_entities(cls) -> Union[List[str], None]:
        return cls.POSSIBLE_ENTITIES

    @classmethod
    def get_possible_regions(cls) -> Union[List[str], None]:
        return cls.POSSIBLE_REGIONS

    @classmethod
    def validate_supported_entities(cls, supported_entities) -> Union[str, List[str]]:
        if (
            not supported_entities
            or not isinstance(supported_entities, list)
            or any([not isinstance(entity, str) for entity in supported_entities])
        ):
            raise ValueError(
                "Argument supported_entities must be a non-empty list of strings. Given: {}.".format(supported_entities)
            )
        if issubclass(cls, PatternRecognizer):
            if len(supported_entities) != 1:
                raise ValueError(
                    "A PatternRecognizer supports exactly one entity. Given: {}.".format(supported_entities)
                )
            else:
                return supported_entities[0]
        return supported_entities


class CustomPatternRecognizer(PatternRecognizer, CustomRecognizerMixin):
    """Base class for pattern recognizers of this library."""

    def __init__(
        self,
        supported_language,
        supported_entities,
        patterns,
        supported_regions,
        words_to_remove_from_match=[],
        trigger_words=[],
        calling_recognizer=None,
    ):
        PatternRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entity=self.validate_supported_entities(supported_entities=supported_entities),  # type: ignore
            patterns=patterns,
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)
        self.words_to_remove_from_match = words_to_remove_from_match
        self.words_to_remove_from_match_regexes = [
            r"\b" + re.escape(word) + r"\b" for word in words_to_remove_from_match
        ]
        self.words_to_remove_from_match_regexes = [
            r"\b" + re.escape(word) + r"\b" for word in words_to_remove_from_match
        ]
        self.trigger_words = trigger_words
        self.trigger_words_regexes = [r"\b" + re.escape(word) + r"\b" for word in trigger_words]
        self.calling_recognizer = calling_recognizer

    def post_process_match(self, match_span, text) -> List[Tuple[int, int]]:
        """
        Post-process match, e.g. by removing words from a denylist.
        Returns valid spans.
        """
        matched_text = text[match_span[0] : match_span[1]]

        # Extract spans to be removed from text.
        spans_to_remove_raw: List = []
        for regex in self.words_to_remove_from_match_regexes:
            for match in re.finditer(regex, matched_text):
                m_start, m_end = match.span()
                spans_to_remove_raw.append((match_span[0] + m_start, match_span[0] + m_end))

        # Post-process spans.
        spans_to_remove_raw.sort(key=lambda x: x[0])
        if spans_to_remove_raw:
            debugging_text = "Post-Process | Raw spans to remove: {}".format(spans_to_remove_raw)
            debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
        spans_to_remove: List = []
        # Handle intersecting spans.
        end_previous_span = -1
        for span in spans_to_remove_raw:
            start_current_span, end_current_span = span[0], span[1]
            start_span_to_add, end_span_to_add = start_current_span, end_current_span

            if start_current_span < end_previous_span:
                # Discard enclosed spans.
                if end_current_span <= end_previous_span:
                    continue
                # Correct overlapping span.
                else:
                    start_span_to_add, end_span_to_add = (
                        end_previous_span,
                        end_current_span,
                    )
                    start_span_to_add, end_span_to_add = (
                        end_previous_span,
                        end_current_span,
                    )

            # Create final span.
            spans_to_remove.append((start_span_to_add, end_span_to_add))

            # Prepare next iteration.
            end_previous_span = end_current_span

        # Create valid spans from list of spans to be removed.
        final_spans: List = []
        if spans_to_remove:
            debugging_text = "Post-Process | Spans to remove: {}".format(spans_to_remove)
            debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
            spans: List = []
            # Add leading span.
            if spans_to_remove[0][0] > match_span[0]:
                spans.append((match_span[0], spans_to_remove[0][0]))

            # Add middle spans.
            for i in range(len(spans_to_remove)):
                if i != len(spans_to_remove) - 1:
                    if spans_to_remove[i][1] != spans_to_remove[i + 1][0]:
                        spans.append((spans_to_remove[i][1], spans_to_remove[i + 1][0]))

            # Add trailing span.
            if spans_to_remove[-1][1] < match_span[1]:
                spans.append((spans_to_remove[-1][1], match_span[1]))

            # Post-process spans.
            # Remove leading and trailing whitespaces from spans.
            whitespace = " "
            for span in spans:
                span_text = text[span[0] : span[1]]
                num_leading_spaces = len(span_text) - len(span_text.lstrip(whitespace))
                num_trailing_spaces = len(span_text) - len(span_text.rstrip(whitespace))
                if num_leading_spaces > 0 or num_trailing_spaces > 0:
                    correct_start = span[0] + num_leading_spaces
                    correct_end = span[1] - num_trailing_spaces
                    if correct_start < correct_end:
                        final_spans.append((correct_start, correct_end))
                else:
                    final_spans.append((span[0], span[1]))

        # Or return original match.
        else:
            final_spans.append((match_span[0], match_span[1]))

        return final_spans

    def analyze(
        self,
        text: str,
        entities: List[str],
        nlp_artifacts: Optional[NlpArtifacts] = None,
        regex_flags: Optional[int] = None,
    ) -> List[RecognizerResult]:
        """
        This is a hard copy of the analyze method of presidio's PatternRecognizer.
        The only change is the addition of the call to the analyze_patterns method.

        Analyzes text to detect PII using regular expressions or deny-lists.

        :param text: Text to be analyzed
        :param entities: Entities this recognizer can detect
        :param nlp_artifacts: Output values from the NLP engine
        :param regex_flags:
        :return:
        """

        results = []

        if self.patterns:
            pattern_result = self.analyze_patterns(text, regex_flags)  # type:ignore

            if pattern_result and self.context:
                # try to improve the results score using the surrounding
                # context words
                enhanced_result = self.enhance_using_context(
                    text, pattern_result, nlp_artifacts, self.context  # type:ignore
                )
                debug_logging(
                    logger=LOGGER, calling_recognizer=self.calling_recognizer, matches=enhanced_result, text=text
                )
                results.extend(enhanced_result)
            elif pattern_result:
                debug_logging(
                    logger=LOGGER, calling_recognizer=self.calling_recognizer, matches=pattern_result, text=text
                )
                results.extend(pattern_result)

        return results

    def analyze_patterns(
        self, text: str, flags: int = None  # type:ignore
    ) -> List[RecognizerResult]:
        """
        This is a hard copy of the __analyze_patterns method of presidio's PatternRecognizer.
        This was necessary to introduce a post-processing step after a pattern match is found,
        e.g. for removal of words form a denylist, and to add the check for trigger words.

        Evaluate all patterns in the provided text.

        Including words in the provided deny-list

        :param text: text to analyze
        :param flags: regex flags
        :return: A list of RecognizerResult
        """
        flags = flags if flags else re.DOTALL | re.MULTILINE | re.VERBOSE
        results = []
        for pattern in self.patterns:
            matches = re.finditer(pattern.regex, text, flags=flags)
            for match in matches:
                debugging_text = "With '{}' pattern found matches: '{}'".format(pattern.name, match.group(0))
                debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
                m_start, m_end = match.span()
                current_match = text[m_start:m_end]

                # Skip empty results
                if current_match == "":
                    debug_logging(
                        logger=LOGGER, log_message="Skipping empty results", calling_recognizer=self.calling_recognizer
                    )
                    continue

                # Check for triggerwords.
                if self.trigger_words and not self.is_surrounded_by_triggerwords(match.span(), text):
                    debugging_text = "Used recognizer: {}".format(self.calling_recognizer)
                    debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
                    debugging_text = (
                        f"Matched '{text[match.start():match.end()]}' but was removed due to missing trigger word."
                    )
                    debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
                    continue

                score = pattern.score

                # Validate match.
                validation_result = self.validate_result(current_match)
                invalidation_result = self.invalidate_result(current_match)

                # Post-process match and generate valid spans.
                spans = self.post_process_match(match.span(), text)
                for start, end in spans:
                    description = self.build_regex_explanation(
                        self.name,
                        pattern.name,
                        pattern.regex,
                        score,
                        validation_result,  # type:ignore
                        flags,
                    )
                    pattern_result = RecognizerResult(self.supported_entities[0], start, end, score, description)

                    if validation_result is not None:
                        if validation_result:
                            pattern_result.score = EntityRecognizer.MAX_SCORE
                        else:
                            pattern_result.score = EntityRecognizer.MIN_SCORE

                    if invalidation_result is not None and invalidation_result:
                        pattern_result.score = EntityRecognizer.MIN_SCORE

                    if pattern_result.score > EntityRecognizer.MIN_SCORE:
                        results.append(pattern_result)

        results = EntityRecognizer.remove_duplicates(results)
        if results:
            debugging_text = "Results of pattern analysis: {}".format(results)
            debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)

        return results

    def is_surrounded_by_triggerwords(self, match_span, text) -> bool:
        """
        Returns True, when the match is surrounded by a trigger word. Returns False otherwise.
        A text window is constructed around the match. If a trigger word is inside the window a match is said to be surrounded by the trigger word.
        The size of the window is measured in chars before and after the match.
        """
        chars_before = 100
        chars_after = 50
        start_idx = match_span[0] - chars_before if match_span[0] - chars_before > 0 else 0
        end_idx = match_span[1] + chars_after if match_span[1] + chars_after < len(text) else len(text)
        text_window = text[start_idx:end_idx]

        for trigger_word_regex in self.trigger_words_regexes:
            if re.search(trigger_word_regex, text_window):
                debugging_text = "Found trigger word regex '{}' in text_window '{}'".format(
                    trigger_word_regex, text_window
                )
                debug_logging(logger=LOGGER, log_message=debugging_text, calling_recognizer=self.calling_recognizer)
                return True

        return False
