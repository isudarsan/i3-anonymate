import pytest
from presidio_analyzer.recognizer_result import RecognizerResult

from tests.conftest import (
    create_clean_person_span_test_parameters,
    create_mock_doc,
    create_mock_nlp_artifacts,
    create_mock_span,
    create_mock_token,
)
from tests.utils import assert_recognizer_result
from text_anonymizer import constants


@pytest.fixture
def nlp_artifacts(mocker):
    text = "Hi this is Mark Watson. Please text me back Sarah."
    text_tokens = [
        "Hi",
        "this",
        "is",
        create_mock_token(mocker, token_text="Mark", pos="NOUN", token_index=3, source_text=text),
        create_mock_token(mocker, token_text="Watson", pos="NOUN", token_index=4, source_text=text),
        ".",
        "Please",
        "text",
        "me",
        "back",
        create_mock_token(mocker, token_text="Sarah", pos="NOUN", token_index=10, source_text=text),
        ".",
    ]

    mock_entities = [
        create_mock_span(mocker, text="Mark Watson", tokens=text_tokens[3:5], label="PERSON"),
        create_mock_span(mocker, text="Sarah", tokens=text_tokens[10:11], label="PERSON"),
    ]
    mock_doc = create_mock_doc(mocker, text=text, doc_tokens=text_tokens)
    mock_nlp_artifacts = create_mock_nlp_artifacts(mocker, mock_entities, mock_doc)
    return mock_nlp_artifacts


class TestCustomPersonRecognizer_RuleEnhancedNER:
    def assert_tokens_check(self, initilized_person_recognizer, span, doc):
        expected_tokens_in_cleaned_span = 1
        cleaned_spans = initilized_person_recognizer._clean_person_span(span, doc)

        assert len(cleaned_spans) == expected_tokens_in_cleaned_span, "Unexpected number of tokens in cleaned span"
        assert cleaned_spans[0].text == "John"

    def test_analyze_no_nlp_artifacts(self, initilized_person_recognizer):
        with pytest.raises(ValueError, match="No nlp_artefacts are provided."):
            initilized_person_recognizer.analyze("Example text.", initilized_person_recognizer.POSSIBLE_ENTITIES)

    def test_analyze_with_valid_entities(self, initilized_person_recognizer, nlp_artifacts):
        text = "Hi this is Mark Watson. Please text me back Sarah."
        result = initilized_person_recognizer.analyze(text, [constants.ENTITY_PERSON], nlp_artifacts)

        assert len(result) > 0
        assert len(result) == 2

        assert_recognizer_result(
            result[0], entity=constants.ENTITY_PERSON, expected_start=11, expected_end=22, expected_score=0.4
        )
        assert_recognizer_result(
            result[1], entity=constants.ENTITY_PERSON, expected_start=44, expected_end=49, expected_score=0.4
        )

    def test_is_match_with_entity(self, initilized_person_recognizer):
        entity = "PERSON"
        correct_label = "PERSON"
        wrong_label = "ADDRESS"

        entity_label_mappings = [({"PERSON", "PER"}, {"PERSON", "PER"})]

        assert initilized_person_recognizer._is_match_with_entity(entity, correct_label, entity_label_mappings)
        assert not initilized_person_recognizer._is_match_with_entity(entity, wrong_label, entity_label_mappings)

    def test_clean_entity_span(self, mocker, initilized_person_recognizer):
        person_entity = constants.ENTITY_PERSON
        non_person_entity = "NOT_A_PERSON"

        text = "Token"
        tokens = [
            create_mock_token(mocker, token_text=text, pos="WRONG_POS", token_index=0, source_text=text, label="PERSON")
        ]
        span = create_mock_span(mocker, text=text, tokens=tokens, label="PERSON")
        doc = create_mock_doc(mocker, text=text, doc_tokens=tokens)

        cleaned_entity_spans_person = initilized_person_recognizer._clean_entity_span(person_entity, span, doc)
        assert len(cleaned_entity_spans_person) == 0

        cleaned_entity_spans_non_person = initilized_person_recognizer._clean_entity_span(non_person_entity, span, doc)
        assert cleaned_entity_spans_non_person[0] == span

    def test_clean_person_span_with_forbidden_chars(self, mocker, initilized_person_recognizer):
        text = "J0hn"
        tokens = [create_mock_token(mocker, token_text=text, pos=None, token_index=0, source_text=text)]
        span = create_mock_span(mocker, text=text, tokens=tokens, label=None)
        doc = create_mock_doc(mocker, text=text, doc_tokens=tokens)

        clean_spans = initilized_person_recognizer._clean_person_span(span, doc)
        assert clean_spans == []

    def test_clean_person_span_with_valid_chars(self, mocker, initilized_person_recognizer):
        text = "John"
        tokens = [
            create_mock_token(mocker, token_text=text, pos="NOUN", token_index=0, source_text=text, label="PERSON")
        ]
        span = create_mock_span(mocker, text=text, tokens=tokens, label="PERSON")
        doc = create_mock_doc(mocker, text=text, doc_tokens=tokens)

        clean_spans = initilized_person_recognizer._clean_person_span(span, doc)

        assert len(clean_spans) == 1

        first_clean_span = clean_spans[0]
        assert first_clean_span.text == span.text
        assert first_clean_span.label_ == span.label_
        assert len(first_clean_span) == len(span)

    def test_clean_person_span_check_too_long_spans(self, mocker, initilized_person_recognizer):
        text = "John John John John John"
        valid_span_length = initilized_person_recognizer.PERSON_MAX_TOKENS
        valid_span_length_tokens = [
            create_mock_token(mocker, token_text="John", pos="NOUN", token_index=i, source_text=text)
            for i in range(valid_span_length)
        ]
        valid_length_span = create_mock_span(mocker, text=text, tokens=valid_span_length_tokens, label="PERSON")
        valid_span_length_doc = create_mock_doc(mocker, text=text, doc_tokens=valid_span_length_tokens)

        cleaned_spans_valid_length = initilized_person_recognizer._clean_person_span(
            valid_length_span, valid_span_length_doc
        )
        assert len(cleaned_spans_valid_length) == 1

        text = "John John John John John John"
        invalid_span_length = initilized_person_recognizer.PERSON_MAX_TOKENS + 1
        invalid_span_length_tokens = [
            create_mock_token(mocker, token_text="John", pos="NOUN", token_index=i, source_text=text)
            for i in range(invalid_span_length)
        ]
        invalid_length_span = create_mock_span(mocker, text=text, tokens=invalid_span_length_tokens, label="PERSON")
        invalid_span_length_doc = create_mock_doc(mocker, text=text, doc_tokens=invalid_span_length_tokens)

        cleaned_spans_invalid_length = initilized_person_recognizer._clean_person_span(
            invalid_length_span, invalid_span_length_doc
        )
        assert len(cleaned_spans_invalid_length) == 0

    def test_clean_person_span_check_tokens(self, mocker, initilized_person_recognizer):
        forbidden_token_character_span, forbidden_token_character_doc = create_clean_person_span_test_parameters(
            mocker, text="John  ", valid_token_text="John"
        )
        self.assert_tokens_check(
            initilized_person_recognizer, forbidden_token_character_span, forbidden_token_character_doc
        )

        wrong_pos_span, wrong_pos_doc = create_clean_person_span_test_parameters(
            mocker, text="John walking", valid_token_text="John", pos="VERB"
        )
        self.assert_tokens_check(initilized_person_recognizer, wrong_pos_span, wrong_pos_doc)

        is_stop_span, is_stop_doc = create_clean_person_span_test_parameters(
            mocker, text="John and", valid_token_text="John", is_stop=True
        )
        self.assert_tokens_check(initilized_person_recognizer, is_stop_span, is_stop_doc)

        denylist_word_span, denylist_word_doc = create_clean_person_span_test_parameters(
            mocker, text="John regards", valid_token_text="John"
        )
        self.assert_tokens_check(initilized_person_recognizer, denylist_word_span, denylist_word_doc)

    def test_create_results_from_entity_span(self, mocker, initilized_person_recognizer):
        text = "John"
        tokens = [
            create_mock_token(mocker, token_text=text, pos="NOUN", token_index=0, source_text=text, label="PERSON")
        ]
        span = create_mock_span(mocker, text=text, tokens=tokens, label="PERSON")
        doc = create_mock_doc(mocker, text=text, doc_tokens=tokens)

        results = initilized_person_recognizer._create_results_from_entity_span(constants.ENTITY_PERSON, span, doc)
        assert len(results) > 0
        assert isinstance(results[0], RecognizerResult)
