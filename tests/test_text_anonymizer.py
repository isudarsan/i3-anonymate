import pytest

from text_anonymizer import TextAnonymizer, constants
from text_anonymizer.exceptions import LanguageDetectionError


class TestTextAnonymizer:
    """Tests for the text_anonymizer module."""

    def test_TextAnonymizer_initialization(self, text_anonymizer_default):
        assert text_anonymizer_default._supported_languages == constants.AVAILABLE_LANGUAGES
        assert text_anonymizer_default._supported_entities == constants.AVAILABLE_ENTITIES
        assert text_anonymizer_default._supported_regions == constants.AVAILABLE_REGIONS

        count_language_models = len(text_anonymizer_default._nlp_engine.models)
        assert len(constants.AVAILABLE_LANGUAGES) == count_language_models

        selected_languages = [constants.LANGUAGE_CODE_DE]
        anonymizer_single_language = TextAnonymizer(supported_languages=selected_languages)
        count_language_models = len(anonymizer_single_language._nlp_engine.models)
        assert len(selected_languages) == count_language_models

    def test_TextAnonymizer_validate_method_arguments(self):
        anonymizer = TextAnonymizer(
            supported_languages=[constants.LANGUAGE_CODE_DE],
            supported_entities=[constants.ENTITY_PERSON],
            supported_regions=[constants.COUNTRY_CODE_GERMANY],
        )
        supported_entities = anonymizer._supported_entities
        supported_regions = anonymizer._supported_regions

        # Test with entities and regions equal None.
        entities_None = None
        regions_None = None
        _, processed_entities, processed_regions, _ = anonymizer._validate_method_arguments(
            language=constants.LANGUAGE_CODE_DE,
            entities=entities_None,
            regions=regions_None,
            technique=constants.TECHNIQUE_REPLACE,
        )
        assert processed_entities == supported_entities
        assert processed_regions == supported_regions

        # Test with unsupported values for language, entity and region.
        unsupported_language = constants.LANGUAGE_CODE_EN
        unsupported_entity = constants.ENTITY_VIN
        unsupported_region = constants.COUNTRY_CODE_GREAT_BRITAIN

        throws_exception = False
        try:
            _, _, _, _ = anonymizer._validate_method_arguments(
                language=unsupported_language,
                entities=[unsupported_entity],
                regions=[unsupported_region],
                technique=constants.TECHNIQUE_REPLACE,
            )
        except:
            throws_exception = True
        finally:
            assert throws_exception

        # Test with unavailable anonymization technique.
        unavailable_technique = "unavailable_technique"

        throws_exception = False
        try:
            _, _, _, _ = anonymizer._validate_method_arguments(
                language=constants.LANGUAGE_CODE_DE,
                entities=supported_entities,
                regions=supported_regions,
                technique=unavailable_technique,
            )
        except:
            throws_exception = True
        finally:
            assert throws_exception

        # Test with supported and available values.
        (
            processed_language,
            processed_entities,
            processed_regions,
            processed_technique,
        ) = anonymizer._validate_method_arguments(
            language=constants.LANGUAGE_CODE_DE,
            entities=supported_entities,
            regions=supported_regions,
            technique=constants.TECHNIQUE_REPLACE,
        )
        assert processed_language == constants.LANGUAGE_CODE_DE
        assert processed_entities == supported_entities
        assert processed_regions == supported_regions
        assert processed_technique == constants.TECHNIQUE_REPLACE
        assert processed_language != unsupported_language
        assert processed_entities != constants.AVAILABLE_ENTITIES
        assert processed_regions != constants.AVAILABLE_REGIONS

        # Test with no tasks specified.
        throws_exception = False
        try:
            _, _, _, _ = anonymizer._validate_method_arguments(
                technique=unavailable_technique, anonymize=False, detect=False
            )
        except:
            throws_exception = True
        finally:
            assert throws_exception

        # Test detect_language - language parameters combinations
        with pytest.raises(
            ValueError, match="When detect_language is set to True, language needs to be set to None. 'de' was given"
        ):
            _, _, _, _ = anonymizer._validate_method_arguments(
                detect_language=True, language="de", technique=constants.TECHNIQUE_REPLACE
            )

        processed_language, _, _, _ = anonymizer._validate_method_arguments(
            detect_language=False, technique=constants.TECHNIQUE_REPLACE
        )
        assert processed_language == constants.LANGUAGE_CODE_DE

        processed_language, _, _, _ = anonymizer._validate_method_arguments(
            detect_language=True, technique=constants.TECHNIQUE_REPLACE
        )
        assert processed_language is None

    def test_apply_language_detection(self, text_anonymizer_default):
        english_text = "Hello Mark, please perform analysis B and send me the report afterwards. Thank you, Sarah"
        german_text = "Hallo Tobi, kannst du bitte Analyse B durchführen und mir den Bericht schicken. Danke Julia"
        spanish_text = "Hola José, por favor realiza análisis B y envíame el informe después. Gracias, Mercédès"
        letvian_text = "Sveiki, Marks, lūdzu, veiciet B analīzi un pēc tam nosūtiet man ziņojumu. Paldies, Sāra"
        slovenian_text = "Pozdravljeni, Mark, izvedite analizo B in mi nato pošljite poročilo. Hvala, Sarah"

        detected_language_en = text_anonymizer_default._apply_language_detection(
            text=english_text, language_detection_probability_distance=0
        )
        assert detected_language_en == constants.LANGUAGE_CODE_EN

        detected_language_de = text_anonymizer_default._apply_language_detection(
            text=german_text, language_detection_probability_distance=0
        )
        assert detected_language_de == constants.LANGUAGE_CODE_DE

        detected_language_es = text_anonymizer_default._apply_language_detection(
            text=spanish_text, language_detection_probability_distance=0
        )
        assert detected_language_es == constants.LANGUAGE_CODE_ES

        with pytest.raises(LanguageDetectionError):
            _ = text_anonymizer_default._apply_language_detection(
                text=letvian_text, language_detection_probability_distance=0
            )
        with pytest.raises(LanguageDetectionError):
            _ = text_anonymizer_default._apply_language_detection(
                text=slovenian_text, language_detection_probability_distance=0
            )

    def test_TextAnonymizer_process(self, text_anonymizer_default, text_anonymizer_en):
        from tests.resources.fake_piis import fake_vin

        text = "This is a VIN: {}.".format(fake_vin)
        language = "en"

        # Test update mechanism for the recognizer registry.
        number_recognizers_fresh = len(text_anonymizer_default._presidio_analyzer.registry.recognizers)  # type: ignore
        # While initializing the pre-defined presidio recognizers are loaded.
        assert number_recognizers_fresh > 0

        result = text_anonymizer_default.process(text=text, language=language, technique=constants.TECHNIQUE_REDACT)
        number_recognizers_all = len(text_anonymizer_default._presidio_analyzer.registry.recognizers)  # type: ignore
        assert number_recognizers_all > 0
        # TODO: Following assertion depends on tests that were run before because of implicit import logic in
        # RecognizerManager and fake recognizers in test resources
        assert number_recognizers_all != number_recognizers_fresh

        result = text_anonymizer_default.process(
            text=text,
            language=language,
            technique=constants.TECHNIQUE_REDACT,
            regions=[constants.COUNTRY_CODE_GREAT_BRITAIN],
        )
        number_recognizers_restricted = len(text_anonymizer_default._presidio_analyzer.registry.recognizers)  # type: ignore
        assert number_recognizers_restricted > 0
        assert number_recognizers_restricted < number_recognizers_all
        assert number_recognizers_restricted != number_recognizers_fresh

        result = text_anonymizer_default.process(text=text, language=language, technique=constants.TECHNIQUE_REDACT)
        number_recognizers_all_2 = len(text_anonymizer_default._presidio_analyzer.registry.recognizers)  # type: ignore
        assert number_recognizers_all_2 == number_recognizers_all

        # Test anonymized text with one anonymization technique.
        result = text_anonymizer_default.process(text=text, language=language, technique=constants.TECHNIQUE_REDACT)
        assert text != result["text"]
        assert len(result["text"]) < len(text)

        # Test anonymized text with another anonymization technique.
        result = text_anonymizer_default.process(text=text, language=language, technique=constants.TECHNIQUE_REPLACE)
        assert text != result["text"]
        assert len(result["text"]) < len(text)

        # Test with single-language-anonymizer
        result = text_anonymizer_en.process(text=text, technique=constants.TECHNIQUE_REPLACE)
        assert text != result["text"]
        assert len(result["text"]) < len(text)

        # Test content of result dictionary with all flags active.
        result = text_anonymizer_default.process(text=text, language=language, anonymize=True, detect=True)
        assert "entities" in result
        assert "text" in result

        # Test content of result dictionary with anonymize flag active only.
        result = text_anonymizer_default.process(text=text, language=language, anonymize=True, detect=False)
        assert "entities" not in result
        assert "text" in result

        # Test content of result dictionary with detect flag active only.
        result = text_anonymizer_default.process(text=text, language=language, anonymize=False, detect=True)
        assert "entities" in result
        assert "text" not in result

    def test_TextAnonymizer_anonymize(self):
        from tests.resources.fake_piis import fake_vin

        anonymizer = TextAnonymizer()
        text = "This is a VIN: {}.".format(fake_vin)
        language = "en"

        # Test update mechanism for the recognizer registry.
        number_recognizers_fresh = len(anonymizer._presidio_analyzer.registry.recognizers)  # type: ignore
        # While initializing the pre-defined presidio recognizers are loaded.
        assert number_recognizers_fresh > 0

        anonymized_text = anonymizer.anonymize(text=text, language=language, technique=constants.TECHNIQUE_REDACT)
        number_recognizers_all = len(anonymizer._presidio_analyzer.registry.recognizers)  # type: ignore
        assert number_recognizers_all > 0
        # TODO: Following assertion depends on tests that were run before because of implicit import logic in
        # RecognizerManager and fake recognizers in test resources
        assert number_recognizers_all != number_recognizers_fresh

        anonymized_text = anonymizer.anonymize(
            text=text,
            language=language,
            technique=constants.TECHNIQUE_REDACT,
            regions=[constants.COUNTRY_CODE_GREAT_BRITAIN],
        )
        number_recognizers_restricted = len(anonymizer._presidio_analyzer.registry.recognizers)  # type: ignore
        assert number_recognizers_restricted > 0
        assert number_recognizers_restricted < number_recognizers_all
        assert number_recognizers_restricted != number_recognizers_fresh

        anonymized_text = anonymizer.anonymize(text=text, language=language, technique=constants.TECHNIQUE_REDACT)
        number_recognizers_all_2 = len(anonymizer._presidio_analyzer.registry.recognizers)  # type: ignore
        assert number_recognizers_all_2 == number_recognizers_all

        # Test output with one anonymization technique.
        anonymized_text = anonymizer.anonymize(text=text, language=language, technique=constants.TECHNIQUE_REDACT)
        assert text != anonymized_text
        assert len(anonymized_text) < len(text)

        # Test output with another anonymization technique.
        anonymized_text = anonymizer.anonymize(text=text, language=language, technique=constants.TECHNIQUE_REPLACE)
        assert text != anonymized_text
        assert len(anonymized_text) < len(text)
