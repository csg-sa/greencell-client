# Copyright (c) 2025 csg-sa

"""MQTT topics utilities for Greencell EVSE integration.

This module defines helpers for building and caching MQTT topics used by
Greencell EVSE devices in Home Assistant.

Features:
- `MQTT_TOPIC_BASE`: root prefix for all topics.
- `get_mqtt_topics(serial_number)`: builds and caches the topics for a device,
  returning an immutable mapping.

Validation:
- Serial number must be a non-empty string without whitespace.
- Invalid characters (`' '`, `'#'`, `'+'`) are rejected.
- Results are cached with functools.lru_cache for efficiency.
- The returned mapping is read-only (MappingProxyType), ensuring safe reuse across the integration.

Typical usage:

    from .mqtt_topics import get_mqtt_topics

    topics = get_mqtt_topics("EVSE123456")
    print(topics["status"])  # -> "/greencell/evse/EVSE123456/status"

"""

from collections.abc import Mapping
from functools import lru_cache
from types import MappingProxyType

MQTT_TOPIC_BASE = "/greencell/evse"
MAX_CACHE_SIZE = 128


@lru_cache(maxsize=MAX_CACHE_SIZE)
def get_mqtt_topics(serial_number: str) -> Mapping[str, str]:
    """Return an immutable mapping of MQTT topics for a given device.

    Keys:
        - current
        - voltage
        - power
        - status
        - device_state

    Args:
        serial_number: Device serial (non-empty str without whitespace)

    Returns:
        Mapping[str, str]: read-only view of topics

    Raises:
        ValueError: If serial_number is invalid.
    """
    if not isinstance(serial_number, str):
        raise ValueError("Invalid serial number: not a string")
    serial = serial_number.strip()
    if not serial:
        raise ValueError("Invalid serial number: empty/whitespace")
    if any(ch in serial for ch in " #+"):
        raise ValueError(f"Invalid serial number for MQTT topic: {serial!r}")

    base = f"{MQTT_TOPIC_BASE}/{serial}"
    topics = {
        "current": f"{base}/current",
        "voltage": f"{base}/voltage",
        "power": f"{base}/power",
        "status": f"{base}/status",
        "device_state": f"{base}/device_state",
    }
    # Return a read-only view of the topics mapping
    return MappingProxyType(topics)
