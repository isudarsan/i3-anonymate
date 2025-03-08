from presidio_analyzer import Pattern

from text_anonymizer import constants
from text_anonymizer.recognizer_base import CustomPatternRecognizer


class CustomLicensePlateRecognizer_AT(CustomPatternRecognizer):
    """
    Recognize license plates from AT using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_LICENSE_PLATE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_AUSTRIA]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_LICENSE_PLATE_AT = Pattern(
        name="pattern_license_plate_at",
        regex=r"(?<![a-zäöüA-ZÖÜÄ0-9,-])(?P<Regular>(([BEGIKLPSW]{1}([ -]{1}| - {1})(([1-9]{1}[0-9]{4}([ -]{1}| - {1})[A-NPR-Z]{1})|([1-9]{1}[0-9]{3}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{0,1})|([1-9]{1}[0-9]{2}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{0,2})|([1-9]{1}[0-9]{1}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{1,2})|([1-9]{1}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{2})))|([A-PR-Z]{2}([ -]{1}| - {1})(([1-9]{1}[0-9]{3}([ -]{1}| - {1})[A-NPR-Z]{1})|([1-9]{1}[0-9]{2}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{0,1})|([1-9]{1}[0-9]{1}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{1,2})|([1-9]{1}([ -]{1}| - {1})[A-NPR-Z]{1}[A-PR-Z]{2})))))(?![a-zäöüA-ZÖÜÄ0-9,-]|(.\d))(?!\s\d)|(?<![a-zäöüA-ZÖÜÄ0-9,-])(?P<Custom>(([BEGIKLPSW]{1}([ -]{1}| - {1})(([A-PR-Z]{5}([ -]{1}| - {1})[1-9]{1})|([A-PR-Z]{4}([ -]{1}| - {1})[1-9]{1}[0-9]{0,1})|([A-PR-Z]{3}([ -]{1}| - {1})[1-9]{1}[0-9]{0,2})|([A-PR-Z]{2}([ -]{1}| - {1})[1-9]{1}[0-9]{0,3})|([A-PR-Z]{1}([ -]{1}| - {1})[1-9]{1}[0-9]{1,4})))|([A-PR-Z]{2}([ -]{1}| - {1})(([A-PR-Z]{4}([ -]{1}| - {1})[1-9]{1})|([A-PR-Z]{3}([ -]{1}| - {1})[1-9]{1}[0-9]{0,1})|([A-PR-Z]{2}([ -]{1}| - {1})[1-9]{1}[0-9]{0,2})|([A-PR-Z]{1}([ -]{1}| - {1})[1-9]{1}[0-9]{1,3})))))(?![a-zäöüA-ZÖÜÄ0-9,]|(.\d))(?!\s\d)|(?<![a-zäöüA-ZÖÜÄ0-9,-])(?P<Police>BP([ -]{1}| - {1})[1-9]{1}[0-9]{2,4})(?![a-zäöüA-ZÖÜÄ0-9,-])(?!\s\d)|(?<![a-zäöüA-ZÖÜÄ0-9,-])(?P<Oldtimer>(([BEGIKLPSW]{1}([ -][1-9]{2,4}([ -]{1}| - {1})H)|([A-PR-Z]{2}([ -]{1}| - {1})[1-9]{1}[0-9]{1,3}([ -]{1}| - {1})H)))(?![A-ZÖÜÄ0-}| - {1})[1-9]{1}[0-9,]))|(?<![A-ZÖÜÄ0-9,-])(?![A-ZÖÜÄ0-9,-])(?!\s\d)|(?<![a-zäöüA-ZÖÜÄ0-9,-])(?<!\d\s)(?P<Special>([O]{1}|[BKNSTVW]{1}[DK]{0,1}|[LG]{1}[DK]{1}|B[BGH]{1}|FV|JW|PT|ZW)([ -]{1}| - {1})[1-9]{1}[0-9]{0,4})(?![a-zäöüA-ZÖÜÄ0-9,/-])(?!\s\d)",
        score=SCORE,
    )  # no A-1111 LPs
    PATTERNS = [PATTERN_LICENSE_PLATE_AT]

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


class CustomLicensePlateRecognizer_CH(CustomPatternRecognizer):
    """
    Recognize license plates from CH using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_LICENSE_PLATE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SWITZERLAND]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_LICENSE_PLATE_CH = Pattern(
        name="pattern_license_plate_ch",
        regex=r"(?<![a-zäöüA-ZÖÜÄ0-9-])(((?P<diplomats>(CD|CC|CD|AT){1}([ -]{1}| - {1})?)(?P<city>AG|AR|AI|BL|BS|BE|FR|GE|GL|GR|JU|LU|NE|NW|OW|SH|SZ|SO|SG|TI|TG|UR|VD|VS|ZG|ZH)([ -]| - )(?P<first_digit_part>[0-9]{1,3})([ -]| - )?(?P<second_digit_part>[0-9]{0,3}))|((?P<Regular>(?P<city_reg>AG|AR|AI|BL|BS|BE|FR|GE|GL|GR|JU|LU|NE|NW|OW|SH|SZ|SO|SG|TI|TG|UR|VD|VS|ZG|ZH))([ -]| - )(?P<first_digit_part_reg>[0-9]{1,3})([ -]| - )?(?P<second_digit_part_reg>[0-9]{0,3})(([ -]| - )?(?P<garage>U))?)|((?P<military>M([ -]{1}| - {1})?)(?P<first_digit_part_mil>[0-9]{2,3})([ -]| - )?(?P<second_digit_part_mil>[0-9]{2,3})))(?![a-zäöüA-ZÖÜÄ0-9-])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_LICENSE_PLATE_CH]

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


class CustomLicensePlateRecognizer_DE(CustomPatternRecognizer):
    """
    Recognize license plates from DE using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_LICENSE_PLATE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GERMANY]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_LICENSE_PLATE_DE = Pattern(
        name="pattern_license_plate_de",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])((?P<Regular>[A-ZÖÜÄ]{1,3}([ -]{1}| - {1})[A-Z]{1,2}([ -]{1}| - {1})[1-9]{1}[0-9]{0,3}[EH]{0,1}))(?![A-ZÖÜÄ0-9,]|(.\d))|(?<![A-ZÖÜÄ0-9-])(?<![\d\s])((?P<Police>[A-Z]{1,3}([ -]{1}| - {1})[1-9]{1}[0-9]{0,1}([ -]{1}| - {1})[1-9]{1}[0-9]{0,3}[E]{0,1}))(?![A-ZÖÜÄ0-9,-])|(?<![A-ZÖÜÄ0-9,])((?P<GOV>[0]{1}([ -]{1}| - {1})[1-9]{1}[0-9]{0,1}([ -]{1}| - {1})[1-9]{1}[0-9]{0,3}[E]{0,1}))(?![A-ZÖÜÄ0-9])|(?<![A-ZÖÜÄ0-9])((?P<Diplomat>(BN|B)([ -]{1}| - {1})[1-9]{1}[0-9]{0,1}([ -]{1}| - {1})[1-9]{1}[0-9]{0,3}[E]{0,1}))(?![A-ZÖÜÄ0-9])|(?<![A-ZÖÜÄ0-9])(?<![\d\s])((?P<Army>[Y]{1}([ -]{1}| - {1})[1-9]{1}[0-9]{0,1}([ -]{0,1}| - {1})[1-9]{1}[0-9]{0,3}))(?![A-ZÄÖÜa-zäöüß0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_LICENSE_PLATE_DE]

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


class CustomLicensePlateRecognizer_ES(CustomPatternRecognizer):
    """
    Recognize license plates from ES using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_LICENSE_PLATE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_SPAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_LICENSE_PLATE_ES = Pattern(
        name="pattern_license_plate_es",
        regex=r"(?<![A-ZÄÖÜa-zäöüß0-9])(?P<CurrentSince2000>[0-9]{4}([ -]{1}| - {1})[A-Z]{3})(?![A-ZÄÖÜa-zäöüß0-9,])|(?<![A-ZÄÖÜa-zäöüß0-9])(?P<OldtimerSpecial>[EH]{1}[ -]{0,1}[0-9]{4}([ -]{1}| - {1})[A-Z]{3})(?![A-ZÄÖÜa-zäöüß0-9,])|(?<![A-ZÄÖÜa-zäöüß0-9])(?P<Diplomatic>([C]{2}|[C]{1}[D]{1})([ -]{1}| - {1})[1-9]{1}[0-9]{0,1}([ -]{1}| - {1})[0-9]{3})(?![A-ZÄÖÜa-zäöüß0-9,])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_LICENSE_PLATE_ES]

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


class CustomLicensePlateRecognizer_GB(CustomPatternRecognizer):
    """
    Recognize license plates from GB using regular expressions.
    """

    POSSIBLE_LANGUAGES = None
    POSSIBLE_ENTITIES = [constants.ENTITY_LICENSE_PLATE]
    POSSIBLE_REGIONS = [constants.COUNTRY_CODE_GREAT_BRITAIN]

    SCORE = constants.DEFAULT_RECOGNIZER_RESULT_SCORE
    PATTERN_LICENSE_PLATE_GB = Pattern(
        name="pattern_license_plate_gb",
        regex=r"(?<![A-ZÖÜÄ0-9])((?P<CurrentSince2001>[A-Z]{2}([ -]{0,1}| - {1})[0-9]{2}([ -]{0,1}| - {1})[A-Z]{3}))(?![A-ZÖÜÄ|0-9/])|(?<![A-ZÖÜÄ0-9])((?P<NothernIreland>([A-Z]{1}[I]{1}[ABGJLW]{1}|[A-Z]{2}[IZ]{1})([ -]{0,1}| - {1})[1-9]{1}[0-9]{0,3}))(?![A-ZÖÜÄ|0-9])|(?<![A-ZÖÜÄ0-9])((?P<Diplomatic>[1-9]{1}[0-9]{2}([ -]{0,1}| - {1})[DX]{1}([ -]{0,1}| - {1})[1-9]{1}[0-9]{2}))(?![A-ZÖÜÄ|0-9])",
        score=SCORE,
    )
    PATTERNS = [PATTERN_LICENSE_PLATE_GB]

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
