import functools
import os
import warnings
from importlib import import_module
from os.path import join
from pkgutil import walk_packages
from types import ModuleType
from typing import Callable, List, Optional, Type

from phonenumbers import PhoneNumberMatch
from presidio_analyzer import RecognizerResult

from text_anonymizer import constants
from text_anonymizer.logging_config import SPECIFIC_RECOGNIZERS


def text_anonymizer_info():
    """Print information about the languages, entities, regions and anonymization techniques covered by this library.
    When constructing a TextAnonymizer instance, you can specify any subset of the printed values as the supported languages, entities and regions.
    When calling the process method of your TextAnonymizer instance, you can specify one of the available anonymization techniques.
    """
    template = """Info:
    available languages: {}
    available entities: {}
    available regions: {}
    available techniques: {}
    """

    info = template.format(
        constants.AVAILABLE_LANGUAGES,
        constants.AVAILABLE_ENTITIES,
        constants.AVAILABLE_REGIONS,
        constants.AVAILABLE_TECHNIQUES,
    )

    print(info)


def process_key_arguments(
    languages: Optional[List[str]] = None,
    entities: Optional[List[str]] = None,
    regions: Optional[List[str]] = None,
) -> tuple[list[str], list[str], list[str]]:
    """Validate the key arguments used in this library.

    Args:
        languages (Optional[list[str]], optional): [description]. Defaults to None.
        entities (Optional[list[str]], optional): [description]. Defaults to None.
        regions (Optional[list[str]], optional): [description]. Defaults to None.

    Returns:
        list[str], list[str], list[str]: valid languages, entities and regions
    """
    if languages is None:
        languages = constants.AVAILABLE_LANGUAGES
    if entities is None:
        entities = constants.AVAILABLE_ENTITIES
    if regions is None:
        regions = constants.AVAILABLE_REGIONS

    error_message_template = "The following {} are available: {}. Given: {}"

    if any([language not in constants.AVAILABLE_LANGUAGES for language in languages]):
        raise ValueError(error_message_template.format("languages", constants.AVAILABLE_LANGUAGES, languages))
    if any([entity not in constants.AVAILABLE_ENTITIES for entity in entities]):
        raise ValueError(error_message_template.format("entities", constants.AVAILABLE_ENTITIES, entities))
    if any([region not in constants.AVAILABLE_REGIONS for region in regions]):
        raise ValueError(error_message_template.format("regions", constants.AVAILABLE_REGIONS, regions))

    return languages, entities, regions


def get_all_subclasses(a_class: Type) -> List:
    all_sub_classes = set(a_class.__subclasses__()).union(
        [subsub for sub in a_class.__subclasses__() for subsub in get_all_subclasses(sub)]
    )
    return list(all_sub_classes)


def load_modules_from_package(package: ModuleType):

    def onerror(name: str):
        raise ModuleNotFoundError("Error importing module %s." % name)

    package_dir = os.path.dirname(os.path.abspath(package.__file__))  # type: ignore
    for _, name, ispkg in walk_packages([package_dir], prefix=package.__name__ + ".", onerror=onerror):
        if not ispkg:
            _ = import_module(name)


def deprecated_method(alternative_method: str) -> Callable:
    """This is a decorator which can be used to mark methods as deprecated. A warning will be emitted, when the method is called.

    Args:
        alternative_method (str): The method to use instead of the deprecated method.

    Returns:
        Callable: The actual decorator for methods.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            warnings.warn(
                "Calling deprecated method '{}'. This method will be removed in later versions of this module. Use method '{}' instead.".format(
                    func.__name__, alternative_method
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapped

    return decorator


def log_and_reraise_exceptions(logger, exception_type=Exception):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type:
                logger.exception("An error occurred in '%s' or one of its sub-methods", func.__name__)
                raise

        return wrapper

    return decorator


def debug_logging(
    logger,
    log_message: str | None = None,
    calling_recognizer: str | None = None,
    matches: list[RecognizerResult] | list[PhoneNumberMatch] | None = None,
    text: str | None = None,
) -> None:
    """
    Manages logging for different debugging cases.

    It is generally expected that either a `log_message` or `matches` and `text` are given.
    Case0: SPECIFIC_RECOGNIZERS contains at least one recognizer which is not the
            given calling_recognizer. -> Log nothing.
    Case1: matches and text are given and matches is not an empty list. -> Log
            calling_recognizer, type of matched entity, and matched entity text.
    Case2: log_message is given. -> Log given message.
    Case3: matches and text are given but matches is an empty list. -> Log nothing.

    Args:
        logger: The logger instance used for logging messages.
        log_message (str | None): Predefined logging message. Defaults to None.
        calling_recognizer (str | None): The name of the recognizer being called if log
            is written within a recognizer class. Defaults to None.
        matches (list[RecognizerResult] | list[PhoneNumberMatch] | None): A list
            of match results from the recognizer. Defaults to None.
        text (str | None): The text being processed which may contain matched entities.
            Defaults to None.
    """
    if SPECIFIC_RECOGNIZERS and (calling_recognizer not in SPECIFIC_RECOGNIZERS):
        return None

    if matches:
        logger.debug("Used recognizer: %s", calling_recognizer)
        for match in matches:
            logger.debug("Matched Entity: %s | %s", text[match.start : match.end], match)
    elif matches is None:
        logger.debug(log_message)
