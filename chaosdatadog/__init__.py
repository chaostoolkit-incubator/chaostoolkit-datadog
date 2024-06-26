import logging
from contextlib import contextmanager
from importlib.metadata import version, PackageNotFoundError
from typing import Generator, List

from chaoslib.discovery.discover import (
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.types import (
    Configuration,
    DiscoveredActivities,
    Discovery,
    Secrets,
)
from datadog_api_client import ApiClient
from datadog_api_client import Configuration as DDCfg

logger = logging.getLogger("chaostoolkit")
try:
    __version__ = version("chaostoolkit-datadog")
except PackageNotFoundError:
    __version__ = "unknown"


@contextmanager
def get_client(
    configuration: Configuration = None, secrets: Secrets = None, **kwargs
) -> Generator[ApiClient, None, None]:
    configuration = configuration or {}
    secrets = secrets or {}

    dd_host = configuration.get("datadog_host", "https://api.datadoghq.com")
    api_key = secrets.get("api_key")
    app_key = secrets.get("app_key")

    keys = None
    if api_key or app_key:
        keys = {"apiKeyAuth": api_key, "appKeyAuth": app_key}

    c = DDCfg(api_key=keys, host=dd_host)
    with ApiClient(c) as api:
        yield api


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover DataDog capabilities from this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-datadog")

    discovery = initialize_discovery_result(
        "chaostoolkit-datadog", __version__, "datadog"
    )
    discovery["activities"].extend(load_exported_activities())

    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions, probes and tolerances
    exposed by this extension.
    """
    activities = []  # type: ignore

    activities.extend(discover_probes("chaosdatadog.slo.probes"))
    activities.extend(discover_probes("chaosdatadog.metrics.probes"))

    return activities
