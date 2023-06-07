from typing import Any, Dict, Literal
from chaoslib.types import Configuration, Secrets
from chaoslib.exceptions import ActivityFailed
from datadog_api_client.v2.api.metrics_api import (
    MetricsApi,
)
from datetime import datetime
from dateutil.relativedelta import relativedelta
from chaosdatadog import get_client

__all__ = ["get_metrics_state"]


def get_metrics_state(
    query: str,
    comparison: Literal['>', '<', '>=', '<=', '=='],
    threshold: float,
    minutes_before: int,
    configuration: Configuration = None,
    secrets: Secrets = None
) -> Dict[str, Any]:
    """
    The next function is to:

    * Query metrics from any time period (timeseries and scalar)
    * Compare the metrics to some treshold in some time.
      Ex.(CPU, Memory, Network)
    * Check is the sum of datapoins is over some value.
      Ex. (requests, errors, custom metrics)

    you can use a comparison to check if some data points in the query
    do not meet the steady state condition

    Ex. cumsum(sum:istio.mesh.request.count.total{kube_service:test,
               response_code:500}.as_count())

    the previous query is a cumulative sum of all the requests with response
    code of 500. if you need to check that in a windows time your application
    has more than 30 http_500 errors you comparison should be >.

    if the treshold with the comparison matches with some data point the
    hypothesis is going to have deviated state.
    """

    with get_client(configuration, secrets) as c:
        api = MetricsApi(c)

    metrics = api.query_metrics(
                    _from=int(
                        (
                         datetime.now() + relativedelta(minutes=-minutes_before)
                        ).timestamp()
                    ),
                    to=int(
                           datetime.now().timestamp()
                    ),
                    query=query,
                )

    metrics = metrics.to_dict()
    series = metrics.get("series", [{}])
    series = series[0] if len(series) > 0 else {}
    point_list = series.get("pointlist", [])
    if point_value_list := [subpoints[1] for subpoints in point_list]:
        return all(eval(f"_ {comparison} threshold") for _ in point_value_list)
    else:
        raise ActivityFailed("The query could not get points")