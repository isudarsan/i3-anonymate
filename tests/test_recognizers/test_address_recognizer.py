import pytest

from tests.utils import assert_recognizer_result
from tests.entity_test_values import (
    address_at_test_cases,
    address_at_test_case_ids,
    address_ch_test_cases,
    address_ch_test_case_ids,
    address_de_test_cases,
    address_de_test_case_ids,
    address_es_test_cases,
    address_es_test_case_ids,
    address_uk_test_cases,
    address_uk_test_case_ids,
    address_us_test_cases,
    address_us_test_case_ids,
)
from text_anonymizer import constants
from text_anonymizer.recognizers.address.address_recognizer import (
    CustomAddressRecognizer_AT,
    CustomAddressRecognizer_CH,
    CustomAddressRecognizer_DE,
    CustomAddressRecognizer_ES,
    CustomAddressRecognizer_GB,
    CustomAddressRecognizer_US,
)


class TestAddressRecognizer:
    entity = constants.ENTITY_ADDRESS
    expected_score = 0.5
    expected_start = 0

    @pytest.mark.parametrize("address_at", address_at_test_cases, ids=address_at_test_case_ids)
    def test_address_at_analyze(self, address_at: str):
        address_at_recognizer = CustomAddressRecognizer_AT(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_AUSTRIA],
        )
        results = address_at_recognizer.analyze(address_at, [self.entity])

        expected_end = self.expected_start + len(address_at)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("address_ch", address_ch_test_cases, ids=address_ch_test_case_ids)
    def test_address_ch_analyze(self, address_ch: str):
        address_ch_recognizer = CustomAddressRecognizer_CH(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SWITZERLAND],
        )
        results = address_ch_recognizer.analyze(address_ch, [self.entity])

        expected_end = self.expected_start + len(address_ch)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("address_de", address_de_test_cases, ids=address_de_test_case_ids)
    def test_address_de_analyze(self, address_de: str):
        address_de_recognizer = CustomAddressRecognizer_DE(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GERMANY],
        )
        results = address_de_recognizer.analyze(address_de, [self.entity])

        expected_end = self.expected_start + len(address_de)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("address_es", address_es_test_cases, ids=address_es_test_case_ids)
    def test_address_es_analyze(self, address_es: str):
        address_es_recognizer = CustomAddressRecognizer_ES(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SPAIN],
        )
        results = address_es_recognizer.analyze(address_es, [self.entity])

        expected_end = self.expected_start + len(address_es)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("address_uk", address_uk_test_cases, ids=address_uk_test_case_ids)
    def test_address_uk_analyze(self, address_uk: str):
        address_uk_recognizer = CustomAddressRecognizer_GB(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GREAT_BRITAIN],
        )
        results = address_uk_recognizer.analyze(address_uk, [self.entity])

        expected_end = self.expected_start + len(address_uk)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("address_us", address_us_test_cases, ids=address_us_test_case_ids)
    def test_address_us_analyze(self, address_us: str):
        address_us_recognizer = CustomAddressRecognizer_US(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_USA],
        )
        results = address_us_recognizer.analyze(address_us, [self.entity])

        expected_end = self.expected_start + len(address_us)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

