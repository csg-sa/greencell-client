# Copyright (c) 2025 csg-sa

"""
Home Assistant access helpers
=============================

Utilities for managing Home Assistant access levels in Greencell EVSE devices.

This module provides:

- :class:`GreencellHaAccessLevel` – enumeration of access levels
  (``DISABLED``, ``READ``, ``EXECUTE``, ``OFFLINE`` [deprecated], ``UNAVAILABLE``).
- :class:`GreencellAccess` – stateful helper that tracks the current level and
  notifies registered listeners.

GreencellAccess API
-------------------
* :meth:`GreencellAccess.update` – set a new level from its string name.
* :meth:`GreencellAccess.register_listener` – add a callback invoked on changes.
* :meth:`GreencellAccess.can_execute` – returns ``True`` when commands are allowed.
* :meth:`GreencellAccess.is_disabled` – returns ``True`` when control is disabled.

.. note::
   ``OFFLINE`` is deprecated and kept for backward compatibility.
   Treat it as ``UNAVAILABLE`` (or ``DISABLED`` depending on your application).

Example
-------
.. code-block:: python

   access = GreencellAccess()
   access.register_listener(lambda: print("access changed:", access.level))
   access.update("READ")
   if access.can_execute():
       send_command()
"""

import json
import logging
from collections.abc import Callable
from enum import auto
from json import JSONDecodeError

from .utils import GreencellEnum, MqttPayload

_LOGGER = logging.getLogger(__name__)


class GreencellHaAccessLevel(GreencellEnum):
    """
    Access level configured on the device for the Home Assistant integration.
    """

    DISABLED = auto()
    """Integration disabled on device; do not read telemetry or send commands."""

    READ = auto()
    """Read-only access; telemetry allowed, commands blocked."""

    EXECUTE = auto()
    """Full access; telemetry and command execution allowed."""

    OFFLINE = auto()
    """.. deprecated:: 1.0.2

       Use :data:`GreencellHaAccessLevel.UNAVAILABLE` instead.
       Kept only for backward compatibility.
    """

    UNAVAILABLE = auto()
    """Integration not provisioned/configured; entity is unavailable."""


class GreencellAccess:
    """Class to manage access levels for Greencell devices."""

    def __init__(self, access_level: GreencellHaAccessLevel) -> None:
        """Initialize the access manager with a starting access level."""
        self._access_level = access_level
        self._listeners: list[Callable[[], None]] = []

    def update(self, new_access_level: str) -> None:
        """Update the access level and notify listeners.

        Args:
            new_access_level: The new access level as a string.
        """
        self._access_level = GreencellHaAccessLevel.__members__.get(
            new_access_level, GreencellHaAccessLevel.DISABLED
        )

        if self._access_level == GreencellHaAccessLevel.OFFLINE:
            _LOGGER.warning("OFFLINE access level is deprecated, using UNAVAILABLE instead.")
            self._access_level = GreencellHaAccessLevel.UNAVAILABLE
        self._notify_listeners()

    def register_listener(self, listener: Callable[[], None]) -> None:
        """Register a listener to be notified of access level changes.

        Args:
            listener: A callable that will be called when the access level changes.
        """
        self._listeners.append(listener)

    def _notify_listeners(self) -> None:
        """Notify all registered listeners of the access level change."""
        for listener in self._listeners:
            listener()

    def can_execute(self) -> bool:
        """Check if the current access level allows execution of commands."""
        return self._access_level == GreencellHaAccessLevel.EXECUTE

    def is_disabled(self) -> bool:
        """Check if the current access level is disabled."""
        return self._access_level in (
            GreencellHaAccessLevel.DISABLED,
            GreencellHaAccessLevel.UNAVAILABLE,
        )

    def on_msg(self, msg: MqttPayload) -> None:
        """Handle incoming messages to update access level.

        Args:
            msg: The message containing the new access level.
        """
        try:
            data = json.loads(msg)
        except JSONDecodeError as ex:
            _LOGGER.warning("Failed to decode JSON message: %s", ex)
            self.update("DISABLED")
            return

        new_access_level = data.get("level", "DISABLED")
        try:
            self.update(new_access_level)
            _LOGGER.debug("Access level updated to %s", new_access_level)
        except KeyError as ex:
            _LOGGER.warning("Invalid access level in message: %s", ex)
        except TypeError as ex:
            _LOGGER.warning("Type error while updating access level: %s", ex)
        except ValueError as ex:
            _LOGGER.warning("Value error while updating access level: %s", ex)
        except AttributeError as ex:
            _LOGGER.warning("Unexpected error while updating access level: %s", ex)
