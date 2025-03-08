import pytest
from tests.utils import assert_recognizer_result
from tests.entity_test_values import (
    credit_card_test_case_ids,
    credit_card_test_cases,
    invalid_credit_card_test_case_ids,
    invalid_credit_card_test_cases,
    email_test_cases,
    iban_test_case_ids,
    iban_test_cases,
    us_driver_license_test_case_ids,
    us_driver_license_test_cases,
    vin_test_cases,
    vin_test_cases_ids,
    imei_test_cases,
    imei_test_case_ids,
    invalid_imei_test_cases,
    invalid_imei_test_cases_ids,
    phonenumber_de_test_cases,
    phonenumber_de_test_cases_ids,
    phonenumber_at_test_cases,
    phonenumber_at_test_cases_ids,
    phonenumber_ch_test_cases,
    phonenumber_ch_test_cases_ids,
    phonenumber_es_test_cases,
    phonenumber_es_test_cases_ids,
    phonenumber_uk_test_cases,
    phonenumber_uk_test_cases_ids,
    phonenumber_us_test_cases,
    phonenumber_us_test_cases_ids,
)
from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomPatternRecognizer
from text_anonymizer.recognizers.credit_card import CustomCreditCardRecognizer
from text_anonymizer.recognizers.driver_license import (
    CustomDriverLicenseRecognizer_AT,
    CustomDriverLicenseRecognizer_CH,
    CustomDriverLicenseRecognizer_DE,
    CustomDriverLicenseRecognizer_GB,
    CustomDriverLicenseRecognizer_US,
)
from text_anonymizer.recognizers.email_address import CustomEmailAddressRecognizer
from text_anonymizer.recognizers.iban_code import CustomIbanCodeRecognizer
from text_anonymizer.recognizers.identity_card import (
    CustomIdentityCardRecognizer_CH,
    CustomIdentityCardRecognizer_DE,
    CustomIdentityCardRecognizer_ES,
    CustomIdentityCardRecognizer_US,
)
from text_anonymizer.recognizers.ip_address import CustomIpAddressRecognizer
from text_anonymizer.recognizers.license_plate import (
    CustomLicensePlateRecognizer_AT,
    CustomLicensePlateRecognizer_CH,
    CustomLicensePlateRecognizer_DE,
    CustomLicensePlateRecognizer_ES,
    CustomLicensePlateRecognizer_GB,
)
from text_anonymizer.recognizers.mac_address import CustomMacAddressRecognizer
from text_anonymizer.recognizers.passport import (
    CustomPassportRecognizer_AT,
    CustomPassportRecognizer_CH,
    CustomPassportRecognizer_DE,
    CustomPassportRecognizer_ES,
    CustomPassportRecognizer_GB,
    CustomPassportRecognizer_US,
)
from text_anonymizer.recognizers.vin import CustomVinRecognizer
from text_anonymizer.recognizers.imei import CustomImeiRecognizer
from text_anonymizer.recognizers.phone_number import CustomPhoneNumberRecognizer


class TestCreditCardRecognizer:
    entity = constants.ENTITY_CREDIT_CARD
    expected_score = 1.0
    expected_start = 0

    @pytest.mark.parametrize("card_number", credit_card_test_cases, ids=credit_card_test_case_ids)
    def test_credit_card_analyze(self, card_number: str):
        credit_card_recognizer = CustomCreditCardRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = credit_card_recognizer.analyze(card_number, [self.entity])

        expected_end = self.expected_start + len(card_number)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)
    
    @pytest.mark.parametrize("invalid_card_number", invalid_credit_card_test_cases, ids=invalid_credit_card_test_case_ids)
    def test_credit_card_analyze_invalid(self, invalid_card_number: str):
        credit_card_recognizer = CustomCreditCardRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = credit_card_recognizer.analyze(invalid_card_number, [self.entity])

        assert len(results) == 0, "Expecting no results for invalid card numbers"

class TestDriversLicenseRecognizers:
    entity = constants.ENTITY_DRIVER_LICENSE

    def get_license_test_result(
        self, license_number_text: str, recognizer_class: CustomPatternRecognizer, language: str, region: str
    ):
        license_recognizer = recognizer_class(
            supported_language=language, supported_entities=[self.entity], supported_regions=[region]
        )
        results = license_recognizer.analyze(license_number_text, [self.entity])
        return results

    def test_at_license(self):
        results = self.get_license_test_result(
            license_number_text="Führerscheinnummer: 12345678",
            recognizer_class=CustomDriverLicenseRecognizer_AT,
            language=constants.LANGUAGE_CODE_DE,
            region=constants.COUNTRY_CODE_AUSTRIA,
        )
        assert_recognizer_result(results[0], self.entity, expected_start=20, expected_end=28, expected_score=0.5)

    def test_ch_license(self):
        results = self.get_license_test_result(
            license_number_text="Führerausweis: 123456789004",
            recognizer_class=CustomDriverLicenseRecognizer_CH,
            language=constants.LANGUAGE_CODE_DE,
            region=constants.COUNTRY_CODE_SWITZERLAND,
        )
        assert_recognizer_result(results[0], self.entity, expected_start=15, expected_end=27, expected_score=0.5)

    def test_de_license(self):
        results = self.get_license_test_result(
            license_number_text="Führerschein: B072RRE2I55",
            recognizer_class=CustomDriverLicenseRecognizer_DE,
            language=constants.LANGUAGE_CODE_DE,
            region=constants.COUNTRY_CODE_GERMANY,
        )
        assert_recognizer_result(results[0], self.entity, expected_start=14, expected_end=25, expected_score=1.0)

    def test_gb_license(self):
        results = self.get_license_test_result(
            license_number_text="Driving licence: MORGA753116SM9IJ 35",
            recognizer_class=CustomDriverLicenseRecognizer_GB,
            language=constants.LANGUAGE_CODE_EN,
            region=constants.COUNTRY_CODE_GREAT_BRITAIN,
        )
        assert_recognizer_result(results[0], self.entity, expected_start=17, expected_end=33, expected_score=0.5)

    @pytest.mark.parametrize("license_number", us_driver_license_test_cases, ids=us_driver_license_test_case_ids)
    def test_us_license(self, license_number: str):
        results = self.get_license_test_result(
            license_number_text=f"driver license: {license_number}",
            recognizer_class=CustomDriverLicenseRecognizer_US,
            language=constants.LANGUAGE_CODE_EN,
            region=constants.COUNTRY_CODE_USA,
        )

        start_license_number = 16
        end_license_number = start_license_number + len(license_number)
        assert_recognizer_result(results[0], self.entity, start_license_number, end_license_number, expected_score=0.5)


class TestEmailAddressRecognizer:
    entity = constants.ENTITY_EMAIL_ADDRESS
    expected_start = 0
    expected_score = 1.0

    @pytest.mark.parametrize("email_address", email_test_cases)
    def test_email_analyze(self, email_address):
        email_recognizer = CustomEmailAddressRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = email_recognizer.analyze(email_address, [self.entity])

        expected_end = self.expected_start + len(email_address)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


class TestIbanCodeRecognizer:
    entity = constants.ENTITY_IBAN_CODE
    expected_start = 0
    expected_score = 1.0

    @pytest.mark.parametrize("iban", iban_test_cases, ids=iban_test_case_ids)
    def test_iban_analyze(self, iban):
        iban_recognizer = CustomIbanCodeRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = iban_recognizer.analyze(iban, [self.entity])

        expected_end = self.expected_start + len(iban)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


class TestIdentityCardRecognizer:
    entity = constants.ENTITY_IDENTITY_CARD

    def test_identity_card_ch(self):
        identity_card_recognizer = CustomIdentityCardRecognizer_CH(
            supported_language=constants.LANGUAGE_CODE_DE,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SWITZERLAND],
        )
        results = identity_card_recognizer.analyze("Identitätskartennummer: S0004156", [self.entity])

        assert_recognizer_result(results[0], self.entity, expected_start=24, expected_end=32, expected_score=0.5)

    def test_identity_card_de(self):
        identity_card_recognizer = CustomIdentityCardRecognizer_DE(
            supported_language=constants.LANGUAGE_CODE_DE,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GERMANY],
        )
        results = identity_card_recognizer.analyze("Personalausweis: T22000129", [self.entity])

        assert_recognizer_result(results[0], self.entity, expected_start=17, expected_end=26, expected_score=0.5)

    def test_identity_card_es(self):
        identity_card_recognizer = CustomIdentityCardRecognizer_ES(
            supported_language=constants.LANGUAGE_CODE_ES,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SPAIN],
        )
        results = identity_card_recognizer.analyze("65004204V", [self.entity])

        assert_recognizer_result(results[0], self.entity, expected_start=0, expected_end=9, expected_score=1.0)

    def test_identity_card_us(self):
        identity_card_recognizer = CustomIdentityCardRecognizer_US(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_USA],
        )
        results = identity_card_recognizer.analyze("SSN: 416 80 0291", [self.entity])

        assert_recognizer_result(results[0], self.entity, expected_start=5, expected_end=16, expected_score=0.5)


class TestIPAddressRecognizer:
    entity = constants.ENTITY_IP_ADDRESS
    expected_start = 0
    expected_score = 0.6

    @pytest.mark.parametrize(
        "ip_address", ["192.168.1.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"], ids=["IPv4", "IPv6"]
    )
    def test_ip_address_analyze(self, ip_address):
        ip_address_recognizer = CustomIpAddressRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = ip_address_recognizer.analyze(ip_address, [self.entity])

        expected_end = self.expected_start + len(ip_address)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


class TestLicensePlateRecognizers:
    entity = constants.ENTITY_LICENSE_PLATE
    expected_start = 0
    expected_score = 0.5

    def run_license_plate_test(
        self, license_plate_text: str, recognizer_class: CustomPatternRecognizer, language: str, region: str
    ):
        license_plate_recognizer = recognizer_class(
            supported_language=language, supported_entities=[self.entity], supported_regions=[region]
        )
        results = license_plate_recognizer.analyze(license_plate_text, entities=[self.entity])
        expected_end = self.expected_start + len(license_plate_text)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    def test_at_license_plate(self):
        self.run_license_plate_test(
            license_plate_text="W 1234 AB",
            recognizer_class=CustomLicensePlateRecognizer_AT,
            language=constants.LANGUAGE_CODE_DE,
            region=constants.COUNTRY_CODE_AUSTRIA,
        )

    def test_ch_license_plate(self):
        self.run_license_plate_test(
            license_plate_text="ZH 123456",
            recognizer_class=CustomLicensePlateRecognizer_CH,
            language=constants.LANGUAGE_CODE_DE,
            region=constants.COUNTRY_CODE_SWITZERLAND,
        )

    def test_de_license_plate(self):
        self.run_license_plate_test(
            license_plate_text="B AB 1234",
            recognizer_class=CustomLicensePlateRecognizer_DE,
            language=constants.LANGUAGE_CODE_DE,
            region=constants.COUNTRY_CODE_GERMANY,
        )

    def test_es_license_plate(self):
        self.run_license_plate_test(
            license_plate_text="1234 BCD",
            recognizer_class=CustomLicensePlateRecognizer_ES,
            language=constants.LANGUAGE_CODE_ES,
            region=constants.COUNTRY_CODE_SPAIN,
        )

    def test_gb_license_plate(self):
        self.run_license_plate_test(
            license_plate_text="AB23 CDE",
            recognizer_class=CustomLicensePlateRecognizer_GB,
            language=constants.LANGUAGE_CODE_EN,
            region=constants.COUNTRY_CODE_GREAT_BRITAIN,
        )


class TestMacAddressRecognizer:
    entity = constants.ENTITY_MAC_ADDRESS
    expected_start = 0
    expected_score = 0.5

    @pytest.mark.parametrize(
        "mac_address", ["00:80:41:ae:fd:7e", "00-80-41-ae-fd-7e"], ids=["colon_separated", "hyphen_separated"]
    )
    def test_ip_address_analyze(self, mac_address):
        ip_address_recognizer = CustomMacAddressRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = ip_address_recognizer.analyze(mac_address, [self.entity])

        expected_end = self.expected_start + len(mac_address)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


class TestPassportRecognizer:
    entity = constants.ENTITY_PASSPORT
    expected_score = 0.5

    def test_passport_at(self):
        passport_recognizer = CustomPassportRecognizer_AT(
            supported_language=constants.LANGUAGE_CODE_DE,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_AUSTRIA],
        )
        passport_string = "Reisepass U1234567"
        results = passport_recognizer.analyze(passport_string, [self.entity])

        assert_recognizer_result(
            results[0],
            self.entity,
            expected_start=10,
            expected_end=len(passport_string),
            expected_score=self.expected_score,
        )

    # def test_passport_ch(self):
    #     passport_recognizer = CustomPassportRecognizer_CH(
    #         supported_language=constants.LANGUAGE_CODE_DE,
    #         supported_entities=[self.entity],
    #         supported_regions=[constants.COUNTRY_CODE_SWITZERLAND],
    #     )
    #     results = passport_recognizer.analyze("", [self.entity])

    #     assert_recognizer_result(results[0], self.entity, expected_start=10, expected_end=32, expected_score=self.expected_score)

    def test_passport_de(self):
        passport_recognizer = CustomPassportRecognizer_DE(
            supported_language=constants.LANGUAGE_CODE_DE,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GERMANY],
        )
        passport_string = "Reisepass C01X00T47"
        results = passport_recognizer.analyze(passport_string, [self.entity])

        assert_recognizer_result(
            results[0],
            self.entity,
            expected_start=10,
            expected_end=len(passport_string),
            expected_score=self.expected_score,
        )

    def test_passport_es(self):
        passport_recognizer = CustomPassportRecognizer_ES(
            supported_language=constants.LANGUAGE_CODE_ES,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SPAIN],
        )
        passport_string = "pasaporte ZAB000254"
        results = passport_recognizer.analyze(passport_string, [self.entity])

        assert_recognizer_result(
            results[0],
            self.entity,
            expected_start=10,
            expected_end=len(passport_string),
            expected_score=self.expected_score,
        )

    def test_passport_gb(self):
        passport_recognizer = CustomPassportRecognizer_GB(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GREAT_BRITAIN],
        )
        passport_string = "passport 108376537"
        results = passport_recognizer.analyze(passport_string, [self.entity])

        assert_recognizer_result(
            results[0],
            self.entity,
            expected_start=9,
            expected_end=len(passport_string),
            expected_score=self.expected_score,
        )

    def test_passport_us(self):
        passport_recognizer = CustomPassportRecognizer_US(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_USA],
        )
        passport_string = "passport E00007730"
        results = passport_recognizer.analyze(passport_string, [self.entity])

        assert_recognizer_result(
            results[0],
            self.entity,
            expected_start=9,
            expected_end=len(passport_string),
            expected_score=self.expected_score,
        )

class TestVinRecognizer:
    entity = constants.ENTITY_VIN
    expected_start = 0
    expected_score = 0.5

    @pytest.mark.parametrize("vin", vin_test_cases, ids=vin_test_cases_ids)
    def test_vin_analyze(self, vin):
        vin_recognizer = CustomVinRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = vin_recognizer.analyze(vin, [self.entity])

        expected_end = self.expected_start + len(vin)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


class TestImeiRecognizer:
    entity = constants.ENTITY_IMEI
    expected_start = 0
    expected_score = 1.0

    @pytest.mark.parametrize("imei", imei_test_cases, ids=imei_test_case_ids)
    def test_imei_analyze(self, imei):
        imei_recognizer = CustomImeiRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = imei_recognizer.analyze(imei, [self.entity])

        expected_end = self.expected_start + len(imei)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("imei_invalid", invalid_imei_test_cases, ids=invalid_imei_test_cases_ids)
    def test_imei_analyze_invalid(self, imei_invalid):
        imei_recognizer = CustomImeiRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.VALID_GLOBALLY],
        )
        results = imei_recognizer.analyze(imei_invalid, [self.entity])

        assert len(results) == 0, "Expecting no results for invalid imei numbers"

class TestPhoneNumberRecognizer:
    entity = constants.ENTITY_PHONE_NUMBER
    expected_start = 0
    expected_score = 0.5

    @pytest.mark.parametrize("phonenumber", phonenumber_de_test_cases, ids=phonenumber_de_test_cases_ids)
    def test_phone_DE(self, phonenumber):
        phonenumber_recognizer = CustomPhoneNumberRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GERMANY],
        )
        results = phonenumber_recognizer.analyze(phonenumber, [self.entity])

        expected_end = self.expected_start + len(phonenumber)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

    @pytest.mark.parametrize("phonenumber", phonenumber_at_test_cases, ids=phonenumber_at_test_cases_ids)
    def test_phone_AT(self, phonenumber):
        phonenumber_recognizer = CustomPhoneNumberRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_AUSTRIA],
        )
        results = phonenumber_recognizer.analyze(phonenumber, [self.entity])

        expected_end = self.expected_start + len(phonenumber)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


    @pytest.mark.parametrize("phonenumber", phonenumber_ch_test_cases, ids=phonenumber_ch_test_cases_ids)
    def test_phone_CH(self, phonenumber):
        phonenumber_recognizer = CustomPhoneNumberRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SWITZERLAND],
        )
        results = phonenumber_recognizer.analyze(phonenumber, [self.entity])

        expected_end = self.expected_start + len(phonenumber)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


    @pytest.mark.parametrize("phonenumber", phonenumber_es_test_cases, ids=phonenumber_es_test_cases_ids)
    def test_phone_ES(self, phonenumber):
        phonenumber_recognizer = CustomPhoneNumberRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_SPAIN],
        )
        results = phonenumber_recognizer.analyze(phonenumber, [self.entity])

        expected_end = self.expected_start + len(phonenumber)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


    @pytest.mark.parametrize("phonenumber", phonenumber_uk_test_cases, ids=phonenumber_uk_test_cases_ids)
    def test_phone_UK(self, phonenumber):
        phonenumber_recognizer = CustomPhoneNumberRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_GREAT_BRITAIN],
        )
        results = phonenumber_recognizer.analyze(phonenumber, [self.entity])

        expected_end = self.expected_start + len(phonenumber)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)


    @pytest.mark.parametrize("phonenumber", phonenumber_us_test_cases, ids=phonenumber_us_test_cases_ids)
    def test_phone_US(self, phonenumber):
        phonenumber_recognizer = CustomPhoneNumberRecognizer(
            supported_language=constants.LANGUAGE_CODE_EN,
            supported_entities=[self.entity],
            supported_regions=[constants.COUNTRY_CODE_USA],
        )
        results = phonenumber_recognizer.analyze(phonenumber, [self.entity])

        expected_end = self.expected_start + len(phonenumber)
        assert_recognizer_result(results[0], self.entity, self.expected_start, expected_end, self.expected_score)

