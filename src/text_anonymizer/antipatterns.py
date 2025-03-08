import regex as re

REGEX_LI_NUMBER = r"(?<![aZ-zZ0-9])([GLN]I\d{2}\.\d{2}-[PN]-\d{6})(?![0-9])"
PATTERN_LI_NUMBER = re.compile(REGEX_LI_NUMBER, flags=re.DOTALL | re.MULTILINE | re.VERBOSE)


def span_intersect(span1_start, span1_end, span2_start, span2_end):
    return (span1_start >= span2_start and span1_start <= span2_end) or (
        span1_end >= span2_start and span1_end <= span2_end
    )
