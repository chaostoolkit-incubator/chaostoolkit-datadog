from typing import Any, Dict

import arrow
from chaoslib.types import Configuration, Secrets
from datadog_api_client.v1.api.service_level_objectives_api import (
    ServiceLevelObjectivesApi,
)
from logzero import logger

from chaosdatadog import get_client

__all__ = ["get_slo", "get_slo_details"]


def get_slo_details(
    slo_id: str, configuration: Configuration = None, secrets: Secrets = None
) -> Dict[str, Any]:
    """
    Get a SLO's details.

    Please visit https://docs.datadoghq.com/api/latest/service-level-objectives/#get-an-slos-details
    for more information on the response payload, which is returned as a
    dictionary.
    """  # noqa: E501
    with get_client(configuration, secrets) as c:
        api = ServiceLevelObjectivesApi(c)
        response = api.get_slo(slo_id=slo_id)

        return response.to_dict()


def get_slo(
    slo_id: str,
    start_period: str = "2 minutes ago",
    end_period: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Get a SLO's history for the given period.

    Periods should be given relative to each other. If `end_period` isn't
    provided it will resolve to now (UTC). `start_period` is always relative
    to `end_period`. You can use a format such as: `"X minutes ago"` for both.

    Please visit https://docs.datadoghq.com/api/latest/service-level-objectives/#get-an-slos-history
    for more information on the response payload, which is returned as a
    dictionary.
    """  # noqa: E501
    with get_client(configuration, secrets) as c:
        api = ServiceLevelObjectivesApi(c)

        now = arrow.utcnow()
        if not end_period:
            end = now
        else:
            end = now.dehumanize(end_period)

        if not start_period:
            start = now
        else:
            start = end.dehumanize(start_period)

        response = api.get_slo_history(
            slo_id=slo_id, from_ts=start.int_timestamp, to_ts=now.int_timestamp
        )

        slo = response.to_dict()
        logger.debug(f"SLO history is: {slo}")
        return slo
