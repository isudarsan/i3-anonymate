def readme_howto_anonymize():
    """Anonymize a text."""
    from text_anonymizer import TextAnonymizer

    text_anonymizer = TextAnonymizer()

    # Anonymize a German text.
    text = "Hallo mein Name ist Michael Schuhmacher."
    result = text_anonymizer.process(text=text, language="de")
    print(result["text"])

    # Anonymize an English text.
    text = "Hello my name is Michael Jackson."
    result = text_anonymizer.process(text=text, language="en")
    print(result["text"])


def readme_howto_anonymize_using_anonymize_method():
    """Anonymize a text."""
    from text_anonymizer import TextAnonymizer

    text_anonymizer = TextAnonymizer()

    # Anonymize a German text.
    text = "Hallo mein Name ist Michael Schuhmacher."
    text_anonymized = text_anonymizer.anonymize(text=text, language="de")
    print(text_anonymized)

    # Anonymize an English text.
    text = "Hello my name is Michael Jackson."
    text_anonymized = text_anonymizer.anonymize(text=text, language="en")
    print(text_anonymized)


def readme_howto_classify_text_and_list_entities():
    """Classify a text and list entities."""
    from text_anonymizer import TextAnonymizer

    text_anonymizer = TextAnonymizer()

    # Process a text with activated 'detect' flag. This will add a list of entities found in the text to the result.
    text = "Please contact customer for support. WDD2121234A123456, phone +49 176 12345678. Regards, Bill :)"
    result = text_anonymizer.process(text=text, language="en", detect=True)

    # Classify text.
    if result["entities"]:
        print("Caution: This text contains personal data!")
    else:
        print("This text does not contain personal data.")

    # Iterate over entities.
    for entity in result["entities"]:
        print(
            '"{}" is a {} found at position {}-{}.'.format(
                text[entity["start"] : entity["end"]],
                entity["type"],
                entity["start"],
                entity["end"],
            )
        )


def readme_howto_print_info():
    """Print available entities, languages, regions and anonymization techniques."""
    from text_anonymizer import text_anonymizer_info

    # When constructing a TextAnonymizer instance, you can specify any subset of the printed values as the supported languages, entities and regions.
    # When calling the anonymize method of your TextAnonymizer instance, you can specify one of the available anonymization techniques.
    text_anonymizer_info()


def readme_howto_restrict_analysis():
    """Restrict analysis to specific languages, entities and regions."""
    from text_anonymizer import TextAnonymizer

    # Set the languages, entities and regions the text anonymizer is intented to be used for.
    # This can be any subset of the available values listed by the text_anonymizer_info function.
    # If set to None, no restriction takes place and all available values are considered.
    supported_languages = ["en"]
    supported_entities = ["PHONE_NUMBER", "PERSON"]
    supported_regions = None

    # Create the text anonymizer and tell it what it is intended to be used for.
    text_anonymizer = TextAnonymizer(
        supported_languages=supported_languages,
        supported_entities=supported_entities,
        supported_regions=supported_regions,
    )

    # Prepare a text for anonymization.
    text = "Please contact customer for support. WDD2121234A123456, phone +49 176 12345678. Regards, Bill :)"

    # Scenario I: Anonymize text without further restriction.
    # Without further arguments the anonymization consideres all supported values of the text anonymizer.
    result = text_anonymizer.process(text=text, language="en")
    # Expected result:
    # 1) the VIN will not be anonymized, since VIN was not specified when constructing the TextAnonymizer instance.
    # 2) the phone number will be anonymized, since PHONE_NUMBER was specified when constructing the TextAnonymizer instance.
    # 3) the person will be anonymized, since PERSON was specified when constructing the TextAnonymizer instance.
    print(result["text"])

    # Scenario II: Anonymize text with further restrictions.
    # To further restrict anonymization you can choose any subset of the supported values of the text anonymizer,
    # i.e. the values specified when constructing the TextAnonymizer instance.
    result = text_anonymizer.process(text=text, language="en", entities=["PHONE_NUMBER"], regions=["GB"])
    # Expected result:
    # 1) the VIN will not be anonymized, since VIN was not specified when constructing the TextAnonymizer instance.
    # 2) the phone number will not be anonymized. PHONE_NUMBER is in the list of entites, but it is a german phone number
    # and DE is not in the list of regions.
    # 3) the person will not be anonymized, since PERSON is not in the list of entities.
    print(result["text"])


def readme_howto_restrict_analysis_using_anonymize_method():
    """Restrict analysis to specific languages, entities and regions."""
    from text_anonymizer import TextAnonymizer

    # Set the languages, entities and regions the text anonymizer is intented to be used for.
    # This can be any subset of the available values listed by the text_anonymizer_info function.
    # If set to None, no restriction takes place and all available values are considered.
    supported_languages = ["en"]
    supported_entities = ["PHONE_NUMBER", "PERSON"]
    supported_regions = None

    # Create the text anonymizer and tell it what it is intended to be used for.
    text_anonymizer = TextAnonymizer(
        supported_languages=supported_languages,
        supported_entities=supported_entities,
        supported_regions=supported_regions,
    )

    # Prepare a text for anonymization.
    text = "Please contact customer for support. WDD2121234A123456, phone +49 176 12345678. Regards, Bill :)"

    # Scenario I: Anonymize text without further restriction.
    # Without further arguments the anonymization consideres all supported values of the text anonymizer.
    text_anonymized = text_anonymizer.anonymize(text=text, language="en")
    # Expected result:
    # 1) the VIN will not be anonymized, since VIN was not specified when constructing the TextAnonymizer instance.
    # 2) the phone number will be anonymized, since PHONE_NUMBER was specified when constructing the TextAnonymizer instance.
    # 3) the person will be anonymized, since PERSON was specified when constructing the TextAnonymizer instance.
    print(text_anonymized)

    # Scenario II: Anonymize text with further restrictions.
    # To further restrict anonymization you can choose any subset of the supported values of the text anonymizer,
    # i.e. the values specified when constructing the TextAnonymizer instance.
    text_anonymized = text_anonymizer.anonymize(text=text, language="en", entities=["PHONE_NUMBER"], regions=["GB"])
    # Expected result:
    # 1) the VIN will not be anonymized, since VIN was not specified when constructing the TextAnonymizer instance.
    # 2) the phone number will not be anonymized. PHONE_NUMBER is in the list of entites, but it is a german phone number
    # and DE is not in the list of regions.
    # 3) the person will not be anonymized, since PERSON is not in the list of entities.
    print(text_anonymized)


def readme_howto_change_anonymization_technique():
    """Change the anonymization technique."""
    from text_anonymizer import TextAnonymizer

    # Set an anonymization technique.
    # This can be any value of the available anonymization techniques
    # listed by the text_anonymizer_info function.
    technique_redact = "redact"
    technique_replace = "replace"

    # Create a text anonymizer.
    text_anonymizer = TextAnonymizer()

    # Prepare a text for anonymization.
    text = "Hallo mein Name ist Michael Schuhmacher."

    # Anonymize text and tell it what anonymization technique to use.
    result = text_anonymizer.process(text=text, language="de", technique=technique_redact)
    print(result["text"])

    result = text_anonymizer.process(text=text, language="de", technique=technique_replace)
    print(result["text"])


def readme_howto_change_anonymization_technique_using_anonymize_method():
    """Change the anonymization technique."""
    from text_anonymizer import TextAnonymizer

    # Set an anonymization technique.
    # This can be any value of the available anonymization techniques
    # listed by the text_anonymizer_info function.
    technique_redact = "redact"
    technique_replace = "replace"

    # Create a text anonymizer.
    text_anonymizer = TextAnonymizer()

    # Prepare a text for anonymization.
    text = "Hallo mein Name ist Michael Schuhmacher."

    # Anonymize text and tell it what anonymization technique to use.
    text_anonymized = text_anonymizer.anonymize(text=text, language="de", technique=technique_redact)
    print(text_anonymized)

    text_anonymized = text_anonymizer.anonymize(text=text, language="de", technique=technique_replace)
    print(text_anonymized)


if __name__ == "__main__":
    print("\n>> readme_howto_anonymize")
    readme_howto_anonymize()

    print("\n>> readme_howto_anonymize_using_anonymize_method")
    readme_howto_anonymize_using_anonymize_method()

    print("\n>> readme_howto_classify_text_and_list_entities")
    readme_howto_classify_text_and_list_entities()

    print("\n>> readme_howto_print_info")
    readme_howto_print_info()

    print("\n>> readme_howto_restrict_analysis")
    readme_howto_restrict_analysis()

    print("\n>> readme_howto_restrict_analysis_using_anonymize_method")
    readme_howto_restrict_analysis_using_anonymize_method()

    print("\n>> readme_howto_change_anonymization_technique")
    readme_howto_change_anonymization_technique()

    print("\n>> readme_howto_change_anonymization_technique_using_anonymize_method")
    readme_howto_change_anonymization_technique_using_anonymize_method()
