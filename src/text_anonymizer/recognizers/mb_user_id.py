"""
This module contains recognizers for MB_USER_ID entities.

All recognizers are deactivated, since their performance does not meet our expectations for publication.
The most common issue is that upper case strings are falsly recognized as MB_USER_IDs (many FPs, low precision). These strings might be codes of a technical system or simply words written with caps lock on.

Your help is needed to improve these recognizers. We are interested in how you approach recognizing MB_USER_IDs.
You can share your solution by opening a PR on GitHub. We are looking forward to it and appreciate your contribution!
To make your start easy, you should make yourself familiar with the recognizers in this module.
They show different ways of tackling the problem and even more they show different Presidio recognizer base classes that can be used for implementation.
The documentation of the CustomRecognizerMixin class gives you even more insights about how to write recognizers for this library.

If you have any questions reach out to us :)

Have fun and good luck!
"""

import re
from typing import List, Tuple

from presidio_analyzer import (
    AnalysisExplanation,
    LocalRecognizer,
    Pattern,
    PatternRecognizer,
    RecognizerResult,
)
from presidio_analyzer.nlp_engine import NlpArtifacts
from spacy.tokens import Doc

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomRecognizerMixin


class CustomMbUserIdRecognizer_PatternBased(PatternRecognizer, CustomRecognizerMixin):
    """
    *** DEACTIVATED ***
    The possible characteristics (class variables named POSSIBLE_*) are set to '[]', so this recognizer is never used by the recognizer manager.

    This recognizer uses a regular expression to recognize MB_USER_IDs. Its class is derived from Presidio´s PatternRecognizer and - like all recognizers of this library - from our CustomRecognizerMixin.
    """

    # TODO: improve performance of this recognizer. Create a PR and ask for approval by the code owners.
    POSSIBLE_LANGUAGES = []  # None
    POSSIBLE_ENTITIES = []  # [constants.ENTITY_MB_USER_ID]
    POSSIBLE_REGIONS = []  # constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_MB_USER_ID = Pattern(
        name="pattern_mb_user_id",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<mb_user_id>[A-Z]{2}[A-Z0-9]{4,6})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_MB_USER_ID]

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        PatternRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entity=self.validate_supported_entities(supported_entities=supported_entities),  # type: ignore
            patterns=self.PATTERNS,
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)


class CustomMbUserIdRecognizer_RuleBased(LocalRecognizer, CustomRecognizerMixin):
    """
    *** DEACTIVATED ***
    The possible characteristics (class variables named POSSIBLE_*) are set to '[]', so this recognizer is never used by the recognizer manager.

    This recognizer uses a rule consisting of a regular expression combined with insights from the nlp engine (spacy) to recognize MB_USER_IDs. Its class is derived from Presidio´s LocalRecognizer and - like all recognizers of this library - from our CustomRecognizerMixin.
    """

    # TODO: improve performance of this recognizer. Create a PR and ask for approval by the code owners.
    POSSIBLE_LANGUAGES = []  # None
    POSSIBLE_ENTITIES = []  # [constants.ENTITY_MB_USER_ID]
    POSSIBLE_REGIONS = []  # constants.VALID_GLOBALLY

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE

    def __init__(
        self,
        supported_language,
        supported_entities,
        supported_regions,
    ):
        if len(supported_entities) != 1:
            raise ValueError(
                "A {} supports exactly one entity. Given: {}.".format(self.__class__.__name__, supported_entities)
            )
        LocalRecognizer.__init__(
            self,
            supported_language=supported_language,
            supported_entities=self.validate_supported_entities(supported_entities=supported_entities),  # type: ignore
        )
        CustomRecognizerMixin.__init__(self, supported_regions=supported_regions)

    def load(self) -> None:
        pass

    def analyze(self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts) -> List[RecognizerResult]:
        results = []

        for entity in entities:
            if entity != self.get_supported_entities()[0]:
                continue
            matches = self._find_matches(doc=nlp_artifacts.tokens)

            for match in matches:
                result = self._get_recognizer_result(match)
                results.append(result)

        return results

    def _find_matches(self, doc: Doc) -> List[Tuple[int, int]]:
        results = []
        re_mb_user_id = r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<mb_user_id>[A-Z]{2}[A-Z0-9]{4,6})(?![A-ZÄÖÜa-zäöüß0-9])"
        prog_mb_user_id = re.compile(re_mb_user_id)
        group_idx = prog_mb_user_id.groupindex["mb_user_id"]

        for token in doc:
            if not token.is_oov:
                continue

            m = prog_mb_user_id.search(string=token.text)
            if m:
                start = token.idx + m.start(group_idx)
                end = token.idx + m.end(group_idx)
                results.append((start, end))

        return results

    def _get_recognizer_result(self, match):
        return RecognizerResult(
            entity_type=self.get_supported_entities()[0],
            start=match[0],
            end=match[1],
            score=self.SCORE,
            analysis_explanation=self._get_analysis_explanation(),
        )

    def _get_analysis_explanation(self):
        return AnalysisExplanation(
            recognizer=self.__class__.__name__,
            original_score=self.SCORE,
            textual_explanation="Recognized using {}.".format(self.__class__.__name__),
        )
