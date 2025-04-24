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
    CONTROL_VALUE = "control_value_C"
    ENERGY = "energy_kWH"
    FLOW = "flow_litre_per_hour"
    HUMIDITY = "humidity_relative_percent"
    INLET_FLOW_TEMPERATURE = "inlet_flow_temperature_C"
    L1_CURRENT = "L1_current_A"
    L1_VOLTAGE = "L1_voltage_V"
    L2_CURRENT = "L2_current_A"
    L2_VOLTAGE = "L2_voltage_V"
    L3_CURRENT = "L3_current_A"
    L3_VOLTAGE = "L3_voltage_V"
    POWER = "power_kW"
    PROCESS_VALUE = "process_value_C"
    PRODUCED_ENERGY = "produced_energy_kWH"
    PRODUCED_POWER = "produced_power_kW"
    RETURN_TEMPERATURE = "return_temperature_C"
    SETPOINT_VALUE = "setpoint_value_C"
    TARGET_TEMPERATURE = "target_temperature_C"
    TEMPERATURE = "temperature_C"

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
