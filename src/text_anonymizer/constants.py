from typing import Any

from lingua import Language
from presidio_anonymizer.entities import OperatorConfig

#################
# language codes (ISO_639-1)
#################
LANGUAGE_CODE_DE = "de"
LANGUAGE_CODE_EN = "en"
LANGUAGE_CODE_ES = "es"

#################
# PII labels
#################
ENTITY_ADDRESS = "ADDRESS"
ENTITY_CREDIT_CARD = "CREDIT_CARD"
ENTITY_DRIVER_LICENSE = "DRIVER_LICENSE"
ENTITY_EMAIL_ADDRESS = "EMAIL_ADDRESS"
ENTITY_IBAN_CODE = "IBAN_CODE"
ENTITY_IDENTITY_CARD = "IDENTITY_CARD"
ENTITY_IMEI = "IMEI"
ENTITY_IP_ADDRESS = "IP_ADDRESS"
ENTITY_LICENSE_PLATE = "LICENSE_PLATE"
ENTITY_MAC_ADDRESS = "MAC_ADDRESS"
ENTITY_PASSPORT = "PASSPORT"
ENTITY_PERSON = "PERSON"
ENTITY_PHONE_NUMBER = "PHONE_NUMBER"
ENTITY_VIN = "VIN"

#################
# country codes (ISO 3166-1 alpha-2)
#################
COUNTRY_CODE_AUSTRIA = "AT"
COUNTRY_CODE_SWITZERLAND = "CH"
COUNTRY_CODE_GERMANY = "DE"
COUNTRY_CODE_SPAIN = "ES"
COUNTRY_CODE_GREAT_BRITAIN = "GB"
COUNTRY_CODE_USA = "US"

#################
# anonymization techniques
#################
TECHNIQUE_REDACT = "redact"
TECHNIQUE_REPLACE = "replace"

#################
# available languages, entites, regions and techniques
#################
AVAILABLE_LANGUAGES = [LANGUAGE_CODE_DE, LANGUAGE_CODE_EN, LANGUAGE_CODE_ES]
AVAILABLE_ENTITIES = [
    ENTITY_ADDRESS,
    ENTITY_CREDIT_CARD,
    ENTITY_DRIVER_LICENSE,
    ENTITY_EMAIL_ADDRESS,
    ENTITY_IBAN_CODE,
    ENTITY_IDENTITY_CARD,
    ENTITY_IMEI,
    ENTITY_IP_ADDRESS,
    ENTITY_LICENSE_PLATE,
    ENTITY_MAC_ADDRESS,
    ENTITY_PASSPORT,
    ENTITY_PERSON,
    ENTITY_PHONE_NUMBER,
    ENTITY_VIN,
]
AVAILABLE_REGIONS = [
    COUNTRY_CODE_AUSTRIA,
    COUNTRY_CODE_SWITZERLAND,
    COUNTRY_CODE_GERMANY,
    COUNTRY_CODE_SPAIN,
    COUNTRY_CODE_GREAT_BRITAIN,
    COUNTRY_CODE_USA,
]
AVAILABLE_TECHNIQUES = [TECHNIQUE_REDACT, TECHNIQUE_REPLACE]


#################
# language detection
#################
SUPPORTED_LINGUA_LANGUAGES = (Language.ENGLISH, Language.GERMAN, Language.SPANISH)
PERFORMANCE_IMPROVEMENT_LINGUA_LANGUAGES = (
    Language.CZECH,
    Language.DUTCH,
    Language.DANISH,
    Language.ITALIAN,
    Language.FRENCH,
    Language.POLISH,
    Language.PORTUGUESE,
    Language.ROMANIAN,
    Language.SWEDISH,
)
LINGUA_LANGUAGES_FOR_DETECTION = SUPPORTED_LINGUA_LANGUAGES + PERFORMANCE_IMPROVEMENT_LINGUA_LANGUAGES


#################
# presidio anonymizer operators
#################
PRESIDIO_ANONYMIZER_OPERATORS = {
    TECHNIQUE_REDACT: {"DEFAULT": OperatorConfig(operator_name="redact")},
    TECHNIQUE_REPLACE: {"DEFAULT": OperatorConfig(operator_name="replace")},
}

#################
# nlp engine
#################
# TODO: Find more appropriate way to save nlp-config values than in constants.py
NLP_MODELS_CONFIGS = [
    {"lang_code": "de", "model_name": "de_core_news_lg"},
    {"lang_code": "en", "model_name": "en_core_web_trf"},
    {"lang_code": "es", "model_name": "es_core_news_lg"},
]

NER_MODEL_CONFIGURATION = {
    "model_to_presidio_entity_mapping": {
        "PER": "PERSON",
        "PERSON": "PERSON",
        "NORP": "NRP",
        "FAC": "LOCATION",
        "LOC": "LOCATION",
        "GPE": "LOCATION",
        "LOCATION": "LOCATION",
        "ORG": "ORGANIZATION",
        "ORGANIZATION": "ORGANIZATION",
        "DATE": "DATE_TIME",
        "TIME": "DATE_TIME",
    },
    "labels_to_ignore": ["MISC"],
}

NLP_ENGINE_CONFIGURATION: dict[str, str | list[dict[str, str]] | dict[str, Any]] = {
    "nlp_engine_name": "spacy",
    "models": NLP_MODELS_CONFIGS,
    "ner_model_configuration": NER_MODEL_CONFIGURATION,
}

#################
# recognizer
#################
DEFAULT_RECOGNIZER_RESULT_SCORE = 0.5
# Set POSSIBLE_REGIONS to this value if the entities the recognizer supports are valid globally and a regional distinction is not desired.
VALID_GLOBALLY = "VALID_GLOBALLY"
