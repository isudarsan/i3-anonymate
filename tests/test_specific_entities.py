from tests.conftest import retrieve_falsely_detected_phone_number


class TestLiNumbers:
    """Class that tests whether li-numbers are falsely detected as phone numbers"""

    @classmethod
    def setup_class(cls):
        cls.li_number = "LI54.10-P-069698"

    def test_only_li_numbers_de(self, text_anonymizer_de):
        text_only_li_number_de = f"Hallo Lena, führst du bitte {self.li_number} durch? \n Danke, Tobias"
        result_only_li_number_de = text_anonymizer_de.process(
            text=text_only_li_number_de, entities=["PHONE_NUMBER"], detect=True
        )
        false_detection = retrieve_falsely_detected_phone_number(
            process_result=result_only_li_number_de, original_text=text_only_li_number_de
        )

        assert (
            not false_detection
        ), f"Phone number is not present but was detected as '{false_detection}' in {result_only_li_number_de['text']}"

    def test_only_li_numbers_en(self, text_anonymizer_en):
        text_only_li_number_en = f"Hello Sarah, please perform {self.li_number} cause 5? \n Thank you, Steve"
        result_only_li_number_en = text_anonymizer_en.process(
            text=text_only_li_number_en, entities=["PHONE_NUMBER"], detect=True
        )
        false_detection = retrieve_falsely_detected_phone_number(
            process_result=result_only_li_number_en, original_text=text_only_li_number_en
        )

        assert (
            not false_detection
        ), f"Phone number is not present but was detected as '{false_detection}' in {result_only_li_number_en['text']}"

    def test_phone_and_li_number_de(self, text_anonymizer_germany):
        text_phone_and_li_number_de = (
            f"Hallo Lena, führst du bitte {self.li_number} durch und rufst mich danach unter"
            " 017631127019 an? \n Danke, Tobias"
        )
        correct_phone_number_coordinates_de = (79, 91)
        correct_phone_number_entity_dict_de = {
            "start": correct_phone_number_coordinates_de[0],
            "end": correct_phone_number_coordinates_de[1],
            "type": "PHONE_NUMBER",
        }

        result_phone_and_li_number_de = text_anonymizer_germany.process(
            text=text_phone_and_li_number_de, entities=["PHONE_NUMBER"], detect=True
        )
        false_detection = retrieve_falsely_detected_phone_number(
            process_result=result_phone_and_li_number_de,
            original_text=text_phone_and_li_number_de,
            correct_phone_num_coordinates=correct_phone_number_coordinates_de,
        )

        assert (
            not false_detection
        ), f"A Phone number was wrongly detected as '{false_detection}' in {result_phone_and_li_number_de['text']}"

        found_entity_dict = result_phone_and_li_number_de["entities"][0]
        assert found_entity_dict == correct_phone_number_entity_dict_de, (
            f"Found entity parameters '{found_entity_dict}' differ from expected "
            f"phone number entity values '{correct_phone_number_entity_dict_de}'"
        )

    def test_phone_and_li_number_en(self, text_anonymizer_en):
        text_phone_and_li_number_en = (
            f"Hello Sarah, please perform {self.li_number} cause 5 and call me after at "
            "1-866-794-1889? \n Thank you, Steve"
        )
        correct_phone_number_coordinates_en = (74, 88)
        correct_phone_number_entity_dict_en = {
            "start": correct_phone_number_coordinates_en[0],
            "end": correct_phone_number_coordinates_en[1],
            "type": "PHONE_NUMBER",
        }

        result_phone_and_li_number_en = text_anonymizer_en.process(
            text=text_phone_and_li_number_en, entities=["PHONE_NUMBER"], detect=True
        )
        false_detection = retrieve_falsely_detected_phone_number(
            process_result=result_phone_and_li_number_en,
            original_text=text_phone_and_li_number_en,
            correct_phone_num_coordinates=correct_phone_number_coordinates_en,
        )

        assert (
            not false_detection
        ), f"A Phone number was wrongly detected as '{false_detection}' in {result_phone_and_li_number_en['text']}"

        found_entity_dict = result_phone_and_li_number_en["entities"][0]
        assert found_entity_dict == correct_phone_number_entity_dict_en, (
            f"Found entity parameters '{found_entity_dict}' differ from expected "
            f"phone number entity values '{correct_phone_number_entity_dict_en}'"
        )
