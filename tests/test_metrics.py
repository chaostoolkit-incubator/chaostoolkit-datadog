from datetime import datetime
from unittest.mock import MagicMock, patch

from dateutil.relativedelta import relativedelta

from chaosdatadog.metrics.probes import get_metrics_state


@patch("datadog_api_client.api_client.rest", autospec=False)
def test_get_metrics_state(mock_get_client):
    query = "query"
    comparison = ">"
    threshold = 40
    minutes_before = 1

    with patch("chaosdatadog.metrics.probes.MetricsApi") as MockMetricsApi:
        api_mock = MagicMock()
        MockMetricsApi.return_value = api_mock

        point_list = [
            [datetime.now().timestamp(), 51],
            [datetime.now().timestamp(), 35],
            [datetime.now().timestamp(), 20],
            [datetime.now().timestamp(), 10],
        ]
        series = {"pointlist": point_list}
        api_mock.query_metrics.return_value.to_dict.return_value = {
            "series": [series]
        }

        result = get_metrics_state(query, comparison, threshold, minutes_before)

    assert result is False

    api_mock.query_metrics.assert_called_once_with(
        _from=int(
            (
                datetime.now() + relativedelta(minutes=-minutes_before)
            ).timestamp()
        ),
        to=int(datetime.now().timestamp()),
        query=query,
    )
