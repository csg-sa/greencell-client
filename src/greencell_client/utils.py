# Copyright (c) 2025 csg-sa

"""
Utilities & enums for the Greencell EVSE client
===============================================

This module provides:

- :data:`GREENCELL_HABU_DEN_SERIAL_PREFIX` – common serial prefix for Habu Den devices.
- :data:`MqttPayload` – type of a raw MQTT payload accepted by the client's parsers.
- :class:`GreencellEnum` – base class for string-valued enums with doc support.
- :class:`GreencellUtils` – helper utilities, e.g. serial validation:

  * :meth:`GreencellUtils.device_is_habu_den` – checks if a serial matches the
    Habu Den format (full regex validation).

Notes
-----
- ``_DocEnumMeta`` is an internal metaclass used by :class:`GreencellEnum` to
  attach per-member documentation; it is not part of the public API.

Example
-------
.. code-block:: python

   from greencell_client.utils import GreencellUtils

   if GreencellUtils.device_is_habu_den("EVGC021A12345678ZM0001"):
       print("Habu Den detected")

"""

import re
from enum import Enum, EnumMeta
from typing import Any, Union

GREENCELL_HABU_DEN_SERIAL_PREFIX = "EVGC02"

# Mirrors the payload types json.loads accepts, and the ones Home Assistant
# hands to an MQTT subscription callback.
MqttPayload = Union[str, bytes, bytearray]


class _DocEnumMeta(EnumMeta):
    """Metaclass for Greencell enums that supports documentation strings."""

    def __new__(
        metacls,
        cls: str,
        bases: tuple[type, ...],
        classdict: Any,
        **kw: Any,
    ) -> "_DocEnumMeta":
        """Create a new enum class with documentation support.
        Args:
            metacls: The metaclass.
            cls: The name of the class.
            bases: The base classes.
            classdict: The class dictionary containing members and their docs.
            **kw: Additional keyword arguments.
        Returns:
            An instance of the enum class with documentation attached.
        """
        docs_map = dict(classdict.get("__docs__", {}))
        enum_cls = super().__new__(metacls, cls, bases, classdict, **kw)

        member: Enum
        for name, member in enum_cls.__members__.items():
            if name in docs_map:
                member.__doc__ = docs_map[name]
        return enum_cls


class GreencellEnum(str, Enum, metaclass=_DocEnumMeta):
    """Base class for Greencell enums with documentation support."""

    def _generate_next_value_(  # type: ignore[override]
        name: str, start: int, count: int, last_values: list[Any]
    ) -> str:
        """Generate the next value for the enum member.
        Args:
            name: The name of the enum member.
            start: The starting value (not used).
            count: The current count of members (not used).
            last_values: The last values of the enum (not used).
        Returns:
            str: The name of the enum member as its value.
        """
        return name


class GreencellUtils:
    """Utility class for Greencell client operations."""

    @staticmethod
    def device_is_habu_den(serial: str) -> bool:
        """Check if the device is a Habu Den based on its serial number.
        Args:
            serial (str): The serial number of the device.
        Returns:
            bool: True if the serial matches the Habu Den format, False otherwise.
        """
        pattern = r"^EVGC021[A-Z][0-9]{8}ZM[0-9]{4}$"
        return bool(re.fullmatch(pattern, serial))
