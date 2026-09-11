"""
EVSE state utilities
====================

Helpers for managing EVSE state in Greencell devices.

This module provides:

- :class:`EvseStateEnum` – enumeration of possible EVSE states
  (``IDLE``, ``CONNECTED``, ``WAITING_FOR_CAR``, ``CHARGING``, ``FINISHED``,
  ``ERROR_CAR``, ``ERROR_EVSE``, ``UNKNOWN``).

- :class:`EvseStateData` – a simple state tracker that:

  * :meth:`EvseStateData.update` – sets state from a string and notifies listeners,
  * :meth:`EvseStateData.can_be_stopped` – returns ``True`` when stopping is allowed
    (``WAITING_FOR_CAR`` or ``CHARGING``),
  * :meth:`EvseStateData.can_be_started` – returns ``True`` when starting is allowed
    (``FINISHED`` or ``CONNECTED``),
  * :meth:`EvseStateData.register_listener` – registers callbacks invoked on change.

Example
-------
.. code-block:: python

   state = EvseStateData()
   state.update("CHARGING")
   if state.can_be_stopped():
       print("You can stop charging now.")
"""

import logging
from collections.abc import Callable
from enum import auto

from .utils import GreencellEnum

_LOGGER = logging.getLogger(__name__)


class EvseStateEnum(GreencellEnum):
    """Enumeration for Greencell EVSE states."""

    IDLE = auto()
    """EVSE is idle and not charging."""

    CONNECTED = auto()
    """EVSE is connected to the network but not charging."""

    WAITING_FOR_CAR = auto()
    """EVSE is waiting for a car to connect before charging."""

    CHARGING = auto()
    """EVSE is actively charging a car."""

    FINISHED = auto()
    """Charging process is finished, EVSE is ready for the next session."""

    ERROR_CAR = auto()
    """An error occurred with the car (e.g., car disconnected unexpectedly)."""

    ERROR_EVSE = auto()
    """An error occurred with the EVSE itself (e.g., hardware failure)."""

    UNKNOWN = auto()
    """EVSE state is unknown or not set."""


class EvseStateData:
    """Simple internal EVSE state tracker (charging / idle)."""

    def __init__(self) -> None:
        """Initialize the EVSE state data tracker."""
        self._state = EvseStateEnum.UNKNOWN
        self._listeners: list[Callable[[], None]] = []
        self._charging = False

    def update(self, new_state: str) -> None:
        """Update the EVSE state based on the received message.

        Args:
            new_state (str): The new state to set for the EVSE.
        """
        # If new_state matches one of the enum names, use it; otherwise fall back to UNKNOWN
        self._state = EvseStateEnum.__members__.get(new_state, EvseStateEnum.UNKNOWN)

        self._notify_listeners()
        _LOGGER.debug("EVSE state updated to %s", new_state)

    def can_be_stopped(self) -> bool:
        """Check if the EVSE is in a state where charging can be stopped
            (when charging process is allowed by user).

        Returns:
            bool: True if the EVSE is in a state where charging can be stopped,
                  False otherwise.
        """
        return self._state in (EvseStateEnum.WAITING_FOR_CAR, EvseStateEnum.CHARGING)

    def can_be_started(self) -> bool:
        """Check if the EVSE is in a state where charging can be started.

        Returns:
            bool: True if the EVSE is in a state where charging can be started,
                  False otherwise.
        """
        return self._state in (EvseStateEnum.FINISHED, EvseStateEnum.CONNECTED)

    def set_charging(self, value: bool) -> None:
        """Set the charging state of the EVSE.

        Args:
            value (bool): True if the EVSE is charging, False otherwise.
        """
        self._charging = value

    def register_listener(self, listener: Callable[[], None]) -> None:
        """Register a listener to be notified of state changes.

        Args:
            listener (Callable[[], None]): A callable that will be called when the state changes.
        """
        self._listeners.append(listener)

    def _notify_listeners(self) -> None:
        """Notify all registered listeners of a state change."""
        for listener in self._listeners:
            listener()
