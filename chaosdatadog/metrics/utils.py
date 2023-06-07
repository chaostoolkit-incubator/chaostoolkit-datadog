import re


def extract_metric_name(query):
    pattern = r"(?::|^)([^{}:]+)(?:{|$)"
    return match.group(1) if (match := re.search(pattern, query)) else None
