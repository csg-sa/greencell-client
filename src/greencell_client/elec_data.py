"""
Electrical data helpers
=======================

Helpers for managing electrical telemetry in Greencell EVSE devices.

This module provides:

- :class:`ElecData3Phase` – stores values for three phases (``l1``, ``l2``, ``l3``) and exposes:
  * :meth:`ElecData3Phase.update_data` – update from a ``dict`` with keys ``l1``/``l2``/``l3``,
  * :meth:`ElecData3Phase.get_value` – read a specific phase value.

- :class:`ElecDataSinglePhase` – stores a single value and exposes:

  * :meth:`ElecDataSinglePhase.update_data` – set/update the value,
  * :meth:`ElecDataSinglePhase.data` – property returning the current value.

Example
-------
.. code-block:: python

   phases = ElecData3Phase()
   phases.update_data({"l1": 10.5, "l2": 10.2})
   print(phases.get_value("l1"))

   power = ElecDataSinglePhase()
   power.update_data(2300)
   print(power.data)
"""


from dataclasses import dataclass, fields
from typing import Optional, Any


@dataclass
class ElecData3Phase:
    """Dataclass storing electrical data (e.g. current or voltage) for 3 phases."""
    l1: Optional[Any] = None
    l2: Optional[Any] = None
    l3: Optional[Any] = None

    def update_data(self, new_data: dict[str, Any]) -> None:
        """Update sensor data if the dictionary contains keys corresponding to the phases.

        Args:
            new_data (dict[str, Any]): Dictionary containing new data for the phases.
        """
        for f in fields(self):
            if f.name in new_data:
                setattr(self, f.name, new_data[f.name])

    def get_value(self, phase: str) -> Optional[Any]:
        """Get the value for a specific phase.

        Args:
            phase (str): The phase to retrieve the value for (e.g., 'l1', 'l2', 'l3').
        Returns:
            Optional[Any]: The value for the specified phase, or None if the phase is invalid.
        Raises:
            ValueError: If the phase is not one of 'l1', 'l2', or 'l3'.
        """
        for f in fields(self):
            if f.name == phase:
                return getattr(self, f.name)
        raise ValueError(f"Invalid phase: {phase}. Valid phases are \
                         {', '.join(f.name for f in fields(self))}.")


@dataclass
class ElecDataSinglePhase:
    """Dataclass storing single-value data like power, etc."""
    value: Optional[Any] = None

    def update_data(self, new_data: Any) -> None:
        """Update the single phase data with new data.

        Args:
            new_data (Any): New data to update the value with.
        """
        self.value = new_data

    @property
    def data(self) -> Optional[Any]:
        """Get the current value of the single phase data.

        Returns:
            Optional[Any]: The current value of the single phase data.
        """
        return self.value
