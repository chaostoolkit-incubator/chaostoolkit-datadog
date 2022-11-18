from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from logzero import logger

__all__ = ["slo_must_be_met"]


def slo_must_be_met(
    threshold: str = "7d", value: Dict[str, Any] = None
) -> bool:
    """
    Checks that the current SLI value of a SLO is higher than its target
    for a given threshold period (`"7d"`, `"30d"`, `"90d"`, `"custom"`).
    """
    data = value.get("data")
    overall = data.get("overall")
    if not overall:
        raise ActivityFailed("SLO does not have a SLI we can validate")

    thresholds = data.get("thresholds", {})
    if threshold not in thresholds:
        raise ActivityFailed(f"SLO is not set with treshold '{threshold}'")

    sli_value = overall.get("sli_value")
    target = thresholds[threshold]["target"]
    logger.debug(f"SLI value = {sli_value} / SLO is: {target} [{threshold}]")
    if sli_value < target:
        raise ActivityFailed(
            "SLO is not meeting its target: "
            f"{sli_value} < {target} [{threshold}]"
        )

    return True
