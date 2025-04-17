"""Ngenic API measurement model."""

from enum import Enum
from typing import Any

import httpx

from .base import NgenicBase


class MeasurementType(Enum):
    """Measurement type enumeration.

    Undocumented in API.
    """

    UNKNOWN = "unknown"
    TEMPERATURE = "temperature_C"
    TARGET_TEMPERATURE = "target_temperature_C"
    HUMIDITY = "humidity_relative_percent"
    CONTROL_VALUE = "control_value_C"
    POWER_KW = "power_kW"
    ENERGY_KWH = "energy_kWH"
    FLOW = "flow_litre_per_hour"
    INLET_FLOW_TEMPERATURE = "inlet_flow_temperature_C"
    RETURN_TEMPERATURE = "return_temperature_C"
    PROCESS_VALUE = "process_value_C"
    SETPOINT_VALUE = "setpoint_value_C"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Measurement(NgenicBase):
    """Ngenic API measurement model."""

    def __init__(
        self,
        session: httpx.AsyncClient,
        json_data: dict[str, Any],
        measurement_type: MeasurementType,
    ) -> None:
        """Initialize the measurement model."""
        self._measurement_type = measurement_type

        super().__init__(session=session, json_data=json_data)

    def get_type(self) -> MeasurementType:
        """Get the measurement type.

        :return:
            measurement type
        :rtype:
            `~ngenic.models.measurement.MeasurementType`
        """
        return self._measurement_type
