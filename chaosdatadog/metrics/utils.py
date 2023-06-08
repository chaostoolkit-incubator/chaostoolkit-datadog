import re

COMPARISON_VALUES = [">", "<", ">=", "<=", "==", "!="]


def extract_metric_name(query):
    pattern = r"(?::|^)([^{}:]+)(?:{|$)"
    match = re.search(pattern, query)
    return match[1] if match else None


def check_comparison_values(comparison):
    if comparison not in COMPARISON_VALUES:
        raise ValueError(
            "Invalid value. Expected one of: '>', '<', '>=', '<=', '==', '!='"
        )


def get_comparison_operator(comparison):
    operators = {
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
    }
    return operators.get(comparison)
