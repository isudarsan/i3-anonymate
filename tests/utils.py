from enum import Enum

from presidio_analyzer.recognizer_result import RecognizerResult

def assert_recognizer_result(
    result: RecognizerResult, entity: str, expected_start: int, expected_end: int, expected_score: float
):
    assert result.entity_type == entity
    assert result.start == expected_start
    assert result.end == expected_end
    assert result.score == expected_score
