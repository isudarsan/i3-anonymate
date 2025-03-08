from typing import Optional

from presidio_analyzer import Pattern

from text_anonymizer import constants, triggerwords
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomDriverLicenseRecognizer_AT(CustomPatternRecognizer):
    """
    Recognize austrian driver license number using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_DRIVER_LICENSE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_AUSTRIA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_DRIVER_LICENSE_AT = Pattern(
        name="pattern_driver_license_at",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<SequentialNumber>([0-9]{8}))(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_DRIVER_LICENSE_AT]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_DRIVER_LICENSE_DE_AT

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
            patterns=self.PATTERNS,
            supported_regions=supported_regions,
            trigger_words=self.TRIGGER_WORDS,
            calling_recognizer=type(self).__name__,
        )


class CustomDriverLicenseRecognizer_CH(CustomPatternRecognizer):
    """
    Recognize swiss driver license number using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_DRIVER_LICENSE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SWITZERLAND]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_DRIVER_LICENSE_CH = Pattern(
        name="pattern_driver_license_ch",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<SequentialNumber>([0-9]{12}))(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_DRIVER_LICENSE_CH]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_DRIVER_LICENSE_DE_CH

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
            patterns=self.PATTERNS,
            supported_regions=supported_regions,
            trigger_words=self.TRIGGER_WORDS,
            calling_recognizer=type(self).__name__,
        )


class CustomDriverLicenseRecognizer_DE(CustomPatternRecognizer):
    """
    Recognize german driver license number using regular expressions and checksum validation.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_DRIVER_LICENSE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GERMANY]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_DRIVER_LICENSE_DE = Pattern(
        name="pattern_driver_license_de:",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<Country>[A-P]{1})(?P<District>[0-9]{3})(?P<SequentialNumber>[A-Z0-9]{5})(?P<Checksum>[X0-9]{1})(?P<Number>[A1-9]{1})(?![A-ZÄÖÜa-zäöüß0-9]|[.A-ZÄÖÜa-zäöüß])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_DRIVER_LICENSE_DE]

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
            patterns=self.PATTERNS,
            supported_regions=supported_regions,
            calling_recognizer=type(self).__name__,
        )

    def validate_result(self, pattern_text: str) -> Optional[bool]:
        """
        Validate the german driver license number.
        """
        # Identify check digit.
        checkdigit = pattern_text[9]

        # Identify required string for calculation.
        requiredstr = pattern_text[:-2]

        # Lists for calculation
        calculation_list = list(requiredstr)
        calculation_list_int = []
        numeric_list = []
        final_list = []

        for i, value in enumerate(calculation_list):
            if value.isalpha():
                numeric_list.insert(i, ord(value) - 55)
            else:
                numeric_list.insert(i, value)

        calculation_list_int = list(map(int, numeric_list))

        # Multiplier for calculation
        multiplier = 9

        # Calculation
        for i, value in enumerate(calculation_list_int):
            final_list.insert(i, value * multiplier)
            multiplier = multiplier - 1

        # Sum all values in list
        total = sum(final_list)

        # Modulo
        modulo = total % 11

        # Verification
        if modulo == 10:
            isvalid = "X" == checkdigit
        elif modulo == int(checkdigit):
            isvalid = True
        else:
            isvalid = False
        return isvalid


class CustomDriverLicenseRecognizer_GB(CustomPatternRecognizer):
    """
    Recognize british driver license number using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_DRIVER_LICENSE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GREAT_BRITAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_DRIVER_LICENSE_GB = Pattern(
        name="pattern_driver_license_gb",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<Surname>([A-Z]{5})|[A-Z]{1}[9]{4}|[A-Z]{2}[9]{3}|[A-Z]{3}[9]{2}|[A-Z]{4}[9]{1})(?P<Birthdate>[0-9]{6})(?P<InitalesFirstName>([A-Z]{2})|(A-Z){1}(9){1})(?P<ArbitraryDigit>[0-9]{1})(?P<CheckDigits>[A-Z0-9]{2})(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_DRIVER_LICENSE_GB]

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
            patterns=self.PATTERNS,
            supported_regions=supported_regions,
            calling_recognizer=type(self).__name__,
        )


class CustomDriverLicenseRecognizer_US(CustomPatternRecognizer):
    """
    Recognize us driver license number using regular expressions.
    https://ntsi.com/drivers-license-format/
    https://success.myshn.net/Skyhigh_Data_Protection/Data_Identifiers/U.S._Driver's_License_Numbers
    https://www.starpointscreening.com/blog/drivers-license-format-by-state/
    http://www.highprogrammer.com/alan/numbers/dl_us_shared.html
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_DRIVER_LICENSE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_USA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_DRIVER_LICENSE_US = Pattern(
        name="pattern_driver_license_us",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Alabama>[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Alaska>[0-9]{7})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Arizona>[0-9]{9}|[A-Z]{1}[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Arkansas>[9]{1}[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<California>[A-Z]{1}[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Colorado>[0-9]{2}[-]{1}[0-9]{3}[-]{1}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Connecticut>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Delaware>[0-9]{7})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Florida>[A-Z]{1}[0-9]{3}[-]{1}[0-9]{3}[-]{1}[0-9]{2}[-]{1}[0-9]{3}[-]{1}[0-9]{1})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Georgia>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Hawaii>[A-Z]{1}[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Idaho>[A-Z]{2}[0-9]{6}[A-Z]{1})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Illinois>[A-Z]{1}[0-9]{3}[-]{1}[0-9]{4}[-]{1}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9--])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Indiana>[A-Z0-9]{1}[0-9]{3}[-]{1}[0-9]{2}[-]{1}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Iowa>[0-9]{9}|[0-9]{3}[A-Z]{2}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<KansasVirginia>[A-Z]{1}[0-9]{2}[-]{1}[0-9]{2}[-]{1}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Kentucky>[A-Z]{1}[0-9]{2}[-]{1}[0-9]{3}[-]{1}[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Louisiana>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Maine>[0-9]{7})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Maryland>[A-Z]{1}[-]{0,1}[0-9]{3}[-]{1}[0-9]{3}[-]{1}[0-9]{3}[-]{1}[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Massachusetts>[A-Z]{1}[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Michigan>[A-Z]{1}[- ]{1}[0-9]{3}[- ]{1}[0-9]{3}[- ]{1}[0-9]{3}[- ]{1}[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Minnesota>[A-Z]{1}[0-9]{12})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Mississippi>[0-9]{3}[-]{1}[0-9]{2}[-]{1}[0-9]{4})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Missouri>[A-Z]{1}[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Montana>([0]{1}[1-9]{1}|[1]{1}[0-2]{1})[0-9]{11})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Nebraska>[A-Z]{1}[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Nevada>[0-9]{10,12})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<NewHampshire>[0-9]{2}[A-Z]{3}[0-9]{5})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<NewJersey>[A-Z]{1}[0-9]{14})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<NewMexico>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<NewYork>[0-9]{3}[- ]{1}[0-9]{3}[- ]{1}[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<NorthCarolina>[0-9]{12})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<NorthDakota>[A-Z]{3}[0-9]{6})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Ohio>[A-Z]{2}[0-9]{6})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Oklahoma>[A-Z]{1}[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Oregon>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Pennsylvania>[0-9]{2}[- ]{1}[0-9]{3}[- ]{1}[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<RhodeIsland>[1-9]{2}[0-9]{5})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<SouthCarolinaUtah>[0-9]{5,11})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<SouthDakotaTexas>[0-9]{8})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Tennessee>[0-9]{9})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Vermont>[0-9]{7}[A-Z]{1})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Washington>[A-Z]{5}[A-Z0-9]{7})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<WestVirginia>[A-Z]{1}[0-9]{6})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Wisconsin>[A-Z]{1}[0-9]{3}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{2})(?![A-ZÄÖÜa-zäöüß0-9-])|(?<![A-ZÄÖÜa-zäöüß0-9-])(?P<Wyoming>[0-9]{6}[-]{1}[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9-])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_DRIVER_LICENSE_US]
    TRIGGER_WORDS = triggerwords.TRIGGERWORDS_DRIVER_LICENSE_EN_US

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
            patterns=self.PATTERNS,
            supported_regions=supported_regions,
            trigger_words=self.TRIGGER_WORDS,
            calling_recognizer=type(self).__name__,
        )
