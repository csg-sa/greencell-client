# Copyright (c) 2025 csg-sa

"""MQTT topics utilities for Greencell EVSE integration.

This module defines helpers for building and caching MQTT topics used by
Greencell EVSE devices in Home Assistant.

Features:

- `MQTT_TOPIC_BASE`: root prefix for all topics.
- `MqttTopic`: string enum naming every topic segment, so callers do not repeat
  bare string literals.
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

from .utils import GreencellEnum

MQTT_TOPIC_BASE = "/greencell/evse"
MAX_CACHE_SIZE = 128


class MqttTopic(GreencellEnum):
    """Topic segments published by Greencell EVSE devices.

    Values are assigned explicitly instead of with ``auto()``: the inherited
    ``_generate_next_value_`` returns the member *name*, which would produce
    uppercase segments. Interpolate ``.value``, never the member itself --
    ``f"{MqttTopic.POWER}"`` renders as ``MqttTopic.POWER``.
    """

    CURRENT = "current"
    """Per-phase current readings."""

    VOLTAGE = "voltage"
    """Per-phase voltage readings."""

    POWER = "power"
    """Instantaneous power draw."""

    STATUS = "status"
    """Device status payload."""

    DEVICE_STATE = "device_state"
    """EVSE state machine value; see :class:`~greencell_client.state.EvseStateEnum`."""


@lru_cache(maxsize=MAX_CACHE_SIZE)
def get_mqtt_topics(serial_number: str) -> Mapping[str, str]:
    """Return an immutable mapping of MQTT topics for a given device.

    Keys:
        One entry per :class:`MqttTopic` member, keyed by its string value, so
        both ``topics["status"]`` and ``topics[MqttTopic.STATUS]`` work.

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
    topics = {topic.value: f"{base}/{topic.value}" for topic in MqttTopic}
    # Return a read-only view of the topics mapping
    return MappingProxyType(topics)
