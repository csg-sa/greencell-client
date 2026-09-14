# Copyright (c) 2025 csg-sa

"""
mqtt_parser.py
==============

Utilities for parsing MQTT messages for the Greencell EVSE client.

This module provides:

- :func:`_get_json_value` – safe JSON extraction with logging.
- :class:`MqttParser` – helpers to map incoming payloads to data objects:

  * :meth:`MqttParser.parse_3phase_msg` – updates :class:`ElecData3Phase`.
  * :meth:`MqttParser.parse_single_phase_msg` – updates :class:`ElecDataSinglePhase`.

All helpers return ``True`` on success and log detailed errors on malformed payloads.

Example
-------
.. code-block:: python

   ok = MqttParser.parse_single_phase_msg(msg, "power", single_phase_data)
   if not ok:
       _LOGGER.warning("Payload ignored due to parsing error")
"""

import json
import logging
from json import JSONDecodeError
from typing import Any

from .elec_data import ElecData3Phase, ElecDataSinglePhase
from .utils import MqttPayload

_LOGGER = logging.getLogger(__name__)


def _get_json_value(data: MqttPayload) -> dict[str, Any]:
    """Extract JSON data from a payload.

    Args:
        data (MqttPayload): The payload containing JSON data.
    Returns:
        dict[str, Any]: Parsed JSON object, or an empty dict if the payload is
        not a JSON object.
    """
    try:
        value = json.loads(data)
    except JSONDecodeError as ex:
        _LOGGER.warning("Invalid JSON payload: %s", ex)
        return {}

    if not isinstance(value, dict):
        _LOGGER.error("Expected a JSON object, got %s", type(value).__name__)
        return {}

    return value


class MqttParser:
    """Parser for MQTT messages related to Greencell EVSE devices."""

    @staticmethod
    def parse_3phase_msg(msg: MqttPayload, ThreePhaseData: ElecData3Phase) -> bool:
        """Parse current data from MQTT message and update the 3Phase data object.

        Args:
            msg: The MQTT message containing current data.
            ThreePhaseData: An instance of ElecData3Phase to update with parsed data.
        Returns:
            bool: True if parsing was successful, False otherwise.
        """
        data = _get_json_value(msg)
        if not data:
            return False

        try:
            ThreePhaseData.update_data(data)
        except (KeyError, TypeError, ValueError, AttributeError) as ex:
            _LOGGER.warning("Failed to update 3-phase data: %r", ex)
            return False
        else:
            return True

    @staticmethod
    def parse_single_phase_msg(
        msg: MqttPayload, key: str, SinglePhaseData: ElecDataSinglePhase
    ) -> bool:
        """Parse current data from MQTT message and update the single phase data object.

        Args:
            msg: The MQTT message containing current data.
            key: The key in the JSON data to extract single phase value.
            SinglePhaseData: An instance of ElecDataSinglePhase to update with parsed data.
        Returns:
            bool: True if parsing was successful, False otherwise.
        """
        data = _get_json_value(msg)
        if not data:
            return False

        value = data.get(key)
        if value is None:
            _LOGGER.error("Key '%s' not found in message: %s", key, msg)
            return False

        try:
            SinglePhaseData.update_data(value)
        except (TypeError, ValueError, AttributeError) as ex:
            _LOGGER.warning("Failed to update single phase data: %r", ex)
            return False
        else:
            return True
