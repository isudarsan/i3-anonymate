import pytest

from text_anonymizer import TextAnonymizer, constants
from text_anonymizer.constants import (
    COUNTRY_CODE_GERMANY,
    COUNTRY_CODE_USA,
    LANGUAGE_CODE_DE,
    LANGUAGE_CODE_EN,
)


@pytest.fixture(scope="session")
def text_anonymizer_default():
    text_anonymizer_default = TextAnonymizer()
    return text_anonymizer_default


@pytest.fixture(scope="session")
def text_anonymizer_germany():
    text_anonymizer_de = TextAnonymizer(
        supported_languages=[LANGUAGE_CODE_DE], supported_regions=[COUNTRY_CODE_GERMANY]
    )
    return text_anonymizer_de


@pytest.fixture(scope="session")
def text_anonymizer_usa():
    text_anonymizer_usa = TextAnonymizer(supported_languages=[LANGUAGE_CODE_EN], supported_regions=[COUNTRY_CODE_USA])
    return text_anonymizer_usa


@pytest.fixture(scope="session")
def text_anonymizer_de():
    text_anonymizer_de = TextAnonymizer(supported_languages=[LANGUAGE_CODE_DE])
    return text_anonymizer_de


@pytest.fixture(scope="session")
def text_anonymizer_en():
    text_anonymizer_en = TextAnonymizer(supported_languages=[LANGUAGE_CODE_EN])
    return text_anonymizer_en


@pytest.fixture(scope="class")
def initilized_person_recognizer():
    """Import of Recognizer class needs to happen within fixture because of import logic in RecognizerManager"""
    from text_anonymizer.recognizers.person.person_recognizer import (
        CustomPersonRecognizer_RuleEnhancedNER,
    )

    supported_language = constants.LANGUAGE_CODE_EN
    supported_entities = [constants.ENTITY_PERSON]
    supported_regions = constants.VALID_GLOBALLY
    return CustomPersonRecognizer_RuleEnhancedNER(supported_language, supported_entities, supported_regions)


@pytest.fixture(scope="class")
def recognizer_manager_unrestricted():
    from tests.resources import recognizer_manager as recognizer_manager_resources
    from text_anonymizer.recognizer_manager import RecognizerManager

    recognizer_manager = RecognizerManager(
        languages=[constants.LANGUAGE_CODE_DE, constants.LANGUAGE_CODE_EN],
        entities=[constants.ENTITY_ADDRESS, constants.ENTITY_PERSON, constants.ENTITY_VIN],
        regions=[constants.COUNTRY_CODE_GERMANY, constants.COUNTRY_CODE_GREAT_BRITAIN],
        recognizer_package=recognizer_manager_resources,
    )
    return recognizer_manager


def retrieve_falsely_detected_phone_number(
    process_result: dict[str, str | list[dict[str, str | int]]],
    original_text: str,
    correct_phone_num_coordinates: None | tuple[int, int] = None,
) -> str | None:
    """Assumes at most one correct phone number in text"""
    for entity_dict in process_result["entities"]:
        entity_start: int = entity_dict["start"]
        entity_end: int = entity_dict["end"]
        if entity_dict["type"] == "PHONE_NUMBER" and (entity_start, entity_end) != correct_phone_num_coordinates:
            falsely_detected_phone_number = original_text[entity_start:entity_end]
            return falsely_detected_phone_number
    return None


# Mocking functions
def create_mock_token(
    mocker,
    token_text: str,
    pos: str,
    is_stop: bool = False,
    token_index: int | None = None,
    source_text: str | None = None,
    label: str | None = None,
):
    """Finding of start_char assumes that token_text appears only once in source_text"""
    token = mocker.MagicMock(text=token_text, pos_=pos, is_stop=is_stop)
    if source_text is not None:
        token.start_char = source_text.find(token_text)
        token.end_char = token.start_char + len(token_text)

    if token_index is not None:
        token.token_index = token_index

    if label is not None:
        token.label_ = label

    token.__str__.return_value = token_text
    token.__repr__ = lambda self: token_text
    return token


def create_mock_span(mocker, text: str, tokens, label: str):
    span = mocker.MagicMock(
        text=text,
        label_=label,
        start=tokens[0].token_index,
        start_char=tokens[0].start_char,
        end_char=tokens[-1].end_char,
    )
    span.__len__.return_value = len(tokens)
    span.__repr__ = lambda self: text

    def mock_token_iter():
        return iter(tokens)

    span.__iter__.side_effect = mock_token_iter
    return span


def create_mock_doc(mocker, text: str, doc_tokens: list):
    doc = mocker.MagicMock()
    doc.__str__.return_value = text
    doc.__repr__ = lambda self: text

    def getitem(key):
        if isinstance(key, slice):
            span_tokens = doc_tokens[key]
            span = create_mock_span(
                mocker,
                text=text[span_tokens[0].start_char : span_tokens[-1].end_char],
                tokens=span_tokens,
                label=span_tokens[0].label_,
            )
            return span
        return doc_tokens[key]  # Token

    doc.__getitem__.side_effect = getitem
    return doc


def create_mock_nlp_artifacts(mocker, entities, tokens):
    nlp_artifacts = mocker.Mock(entities=entities, tokens=tokens)
    return nlp_artifacts


def create_clean_person_span_test_parameters(
    mocker, text, valid_token_text, pos="NOUN", is_stop=False, token_index=1, label="PERSON"
):
    valid_token = create_mock_token(
        mocker, token_text=valid_token_text, pos="NOUN", token_index=0, source_text=text, label="PERSON"
    )
    invalid_token_text = text.replace(valid_token_text, "").replace(" ", "", 1)

    tokens = [
        valid_token,
        create_mock_token(
            mocker,
            token_text=invalid_token_text,
            pos=pos,
            is_stop=is_stop,
            token_index=token_index,
            source_text=text,
            label=label,
        ),
    ]

    invalid_token_span = create_mock_span(mocker, text, tokens, label="PERSON")
    invalid_token_doc = create_mock_doc(mocker, text, tokens)

    return invalid_token_span, invalid_token_doc
