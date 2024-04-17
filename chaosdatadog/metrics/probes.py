import logging
from datetime import datetime

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from datadog_api_client.exceptions import ApiTypeError, NotFoundException
from datadog_api_client.v1.api.metrics_api import MetricsApi
from dateutil.relativedelta import relativedelta

from chaosdatadog import get_client
from chaosdatadog.metrics.utils import (
    check_comparison_values,
    extract_metric_name,
    get_comparison_operator,
)

__all__ = ["get_metrics_state"]
logger = logging.getLogger("chaostoolkit")


def get_metrics_state(
    query: str,
    comparison: str,
    threshold: float,
    minutes_before: int,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    The next function is to:

    * Query metrics from any time period (timeseries and scalar)
    * Compare the metrics to some treshold in some time.
      Ex.(CPU, Memory, Network)
    * Check is the sum of datapoins is over some value.
      Ex. (requests, errors, custom metrics)

    you can use a comparison to check if all data points in the query
    satisfy the steady state condition

    Ex. cumsum(sum:istio.mesh.request.count.total{kube_service:test,
               response_code:500}.as_count())

    the above query is a cumulative sum of all requests with response
    code of 500. if you want your request in a window of time
    you have a deviant hypothesis if you have more than 30 http_500 errors
    the comparison should be <. so any value below 30 is a steady state.

    the allowed comparison values are [">", "<", ">=", "<=", "=="]

    """

    try:
        check_comparison_values(comparison)
    except ValueError as e:
        raise ActivityFailed(e)

    with get_client(configuration, secrets) as c:
        api = MetricsApi(c)

        metric_name = extract_metric_name(query)

        try:
            api.get_metric_metadata(metric_name)
        except NotFoundException as e:
            logger.debug(e)
            raise ActivityFailed("The metric name doesn't exist !")
        except ApiTypeError as e:
            logger.debug(e)
            raise ActivityFailed("The metric name wasn't in datadog format!")

        metrics = api.query_metrics(
            _from=int(
                (
                    datetime.now() + relativedelta(minutes=-minutes_before)
                ).timestamp()
            ),
            to=int(datetime.now().timestamp()),
            query=query,
        )

        metrics = metrics.to_dict()
        series = metrics.get("series", [{}])
        if not series:
            point_list = [
                [datetime.now().timestamp(), 0],
            ]
            series = [{"pointlist": point_list}]
        series = series[0] if len(series) > 0 else {}
        point_list = series.get("pointlist", [])
        point_value_list = [subpoints[1] for subpoints in point_list]
        compare_function = get_comparison_operator(comparison)
        return all(compare_function(_, threshold) for _ in point_value_list)
