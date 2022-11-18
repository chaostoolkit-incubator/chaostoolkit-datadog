# -*- coding: utf-8 -*-
import json
from unittest.mock import MagicMock, patch

from chaosdatadog.slo.probes import get_slo


@patch("datadog_api_client.api_client.rest", autospec=False)
def test_get_slo(rest):
    r = MagicMock()
    r.getheader.return_value = None
    r.data = json.dumps({}).encode("utf-8")
    cl = MagicMock()
    cl.request.return_value = r
    cl.configuration.unstable_operations = {"get_slo_history": False}
    rest.RESTClientObject.return_value = cl

    results = get_slo(slo_id="slo1")
    assert results == {}
