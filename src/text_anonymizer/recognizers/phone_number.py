import logging
from typing import List, Optional, Union

import phonenumbers
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE, SUPPORTED_REGIONS, Leniency
from phonenumbers.geocoder import country_name_for_number
from presidio_analyzer import AnalysisExplanation, LocalRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts

from text_anonymizer import antipatterns, constants
from text_anonymizer.logging_config import SPECIFIC_RECOGNIZERS
from text_anonymizer.recognizer_base import CustomRecognizerMixin
from text_anonymizer.utils import debug_logging

LOGGER = logging.getLogger(__name__)


class CustomPhoneNumberRecognizer(LocalRecognizer, CustomRecognizerMixin):
    """
    Recognize phone numbers using the phonenumbers library. Inspired by Presidio´s pre-defined PhoneRecognizer class.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_PHONE_NUMBER]
    POSSIBLE_REGIONS = [
        constants.COUNTRY_CODE_AUSTRIA,
        constants.COUNTRY_CODE_GERMANY,
        constants.COUNTRY_CODE_GREAT_BRITAIN,
        constants.COUNTRY_CODE_SPAIN,
        constants.COUNTRY_CODE_SWITZERLAND,
        constants.COUNTRY_CODE_USA,
    ]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    CONTEXT = [
        "phone",
        "number",
        "telephone",
        "cell",
        "cellphone",
        "mobile",
        "call",
        "Telefonummer",
        "Telefonnr.",
        "Telefonnr",
        "Telefon",
        "Tel",
        "Tel.",
        "teléfono",
        "número",
    ]

    def __init__(self, supported_language, supported_entities, supported_regions):
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

    def analyze(
        self,
        text: str,
        entities: List[str],
        nlp_artifacts: NlpArtifacts = None,  # type: ignore
    ) -> List[RecognizerResult]:
        results = []
        for entity in entities:
            if entity != self.get_supported_entities()[0]:
                continue

            # Match international phone numbers (those with a leading +) with high leniency/less strict (leniency=Leniency.POSSIBLE).
            # But only international ones, otherwise many numeric codes will be matched.
            # Leniency.VALID => phone numbers without regional code are rejected.
            # Leniency.POSSIBLE => Validates lenght and accepts numbers without regional code. Accepts two-digit numbers as German phone numbers.
            for match in phonenumbers.PhoneNumberMatcher(text=text, region=None, leniency=Leniency.POSSIBLE):
                if self._matches_supported_region(match):
                    result = self._get_international_recognizer_result(match)
                    debug_logging(logger=LOGGER, calling_recognizer=type(self).__name__, matches=[match], text=text)
                    results.append(result)

            for region in self.get_supported_regions():
                region = self._align_between_libraries(region)
                if region:
                    # Match phone numbers for considered region with low leniency/more strict (leniency=Leniency.STRICT_GROUPING).
                    # Details: https://github.com/daviddrysdale/python-phonenumbers/blob/dev/python/phonenumbers/phonenumbermatcher.py
                    for match in phonenumbers.PhoneNumberMatcher(
                        text=text, region=region, leniency=Leniency.STRICT_GROUPING
                    ):
                        if self._matches_supported_region(match):
                            international_phone_prefix = match.raw_string.startswith("+")  # type: ignore
                            if international_phone_prefix:
                                result = self._get_international_recognizer_result(match)
                            else:
                                result = self._get_regional_recognizer_result(match, text, nlp_artifacts)
                            if result not in results:
                                results.append(result)
                                if SPECIFIC_RECOGNIZERS and type(self).__name__ not in SPECIFIC_RECOGNIZERS:
                                    continue
                                LOGGER.debug("Used recognizer: %s", type(self).__name__)
                                LOGGER.debug(
                                    "Matched Entity for region %s: %s | %s",
                                    region,
                                    text[match.start : match.end],
                                    match,
                                )

        results = self._filter_out_li_numbers(results, text)

        return results

    def _align_between_libraries(self, region: str) -> Union[str, None]:
        if region not in SUPPORTED_REGIONS:
            return None
        return region

    def _matches_supported_region(self, match) -> bool:
        main_region_code = COUNTRY_CODE_TO_REGION_CODE.get(match.number.country_code)[0]  # type: ignore
        return main_region_code in self.supported_regions

    def _get_regional_recognizer_result(self, match, text, nlp_artifacts):
        number = match.number
        main_region_code = COUNTRY_CODE_TO_REGION_CODE.get(number.country_code)[0]  # type: ignore
        result = RecognizerResult(
            entity_type=self.get_supported_entities()[0],
            start=match.start,
            end=match.end,
            score=self.SCORE,
            analysis_explanation=self._get_analysis_explanation(),
        )
        region_specific_context = (
            self.CONTEXT + [main_region_code] + [country_name_for_number(number, self.supported_language)]
        )
        return self.enhance_using_context(text, [result], nlp_artifacts, region_specific_context)[0]

    def _get_international_recognizer_result(self, match):
        return RecognizerResult(
            entity_type=self.get_supported_entities()[0],
            start=match.start,
            end=match.end,
            score=self.SCORE,
            analysis_explanation=self._get_analysis_explanation(),
        )

    def _get_analysis_explanation(self):
        return AnalysisExplanation(
            recognizer=self.__class__.__name__,
            original_score=self.SCORE,
            textual_explanation="Recognized using {}.".format(self.__class__.__name__),
        )

    @staticmethod
    def _filter_out_li_numbers(results: list[RecognizerResult], text: str) -> list[RecognizerResult]:
        """Removes falsely as phone numbers detected li numbers from results"""
        li_matches = [match for match in antipatterns.PATTERN_LI_NUMBER.finditer(text)]
        for result in results:
            for li_match in li_matches:
                li_match_start, li_match_end = li_match.span()
                if antipatterns.span_intersect(li_match_start, li_match_end, result.start, result.end):
                    results.remove(result)
        return results
