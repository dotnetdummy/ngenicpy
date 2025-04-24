"""Node model."""

import asyncio
from enum import Enum
from typing import Any

import httpx

from ..const import API_PATH  # noqa: TID252
from .base import NgenicBase
from .measurement import Measurement, MeasurementType
from .node_status import NodeStatus


class NodeType(Enum):
    """Node type enumeration."""

    UNKNOWN = -1
    SENSOR = 0
    CONTROLLER = 1
    GATEWAY = 2
    INTERNAL = 3
    ROUTER = 4

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Node(NgenicBase):
    """Ngenic API node model."""

    def __init__(
        self, session: httpx.AsyncClient, json_data: dict[str, Any], tune_uuid: str
    ) -> None:
        """Initialize the node model."""
        self._parent_tune_uuid = tune_uuid

        # A cache for measurement types
        self._measurement_types = None

        super().__init__(session=session, json_data=json_data)

    def get_type(self):
        """Get the node type."""
        return NodeType(self["type"])

    def measurement_types(
        self, invalidate_cache: bool = False
    ) -> list[MeasurementType]:
        """Get types of available measurements for this node (async).

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of measurement type enums
        :rtype:
            `list(~ngenic.models.measurement.MeasurementType)
        """
        if not self._measurement_types:
            url = API_PATH["measurements_types"].format(
                tune_uuid=self._parent_tune_uuid, node_uuid=self.uuid()
            )
            measurements = self._parse(self._get(url, invalidate_cache))
            self._measurement_types = [MeasurementType(m) for m in measurements]

        return self._measurement_types

    async def async_measurement_types(
        self, invalidate_cache: bool = False
    ) -> list[MeasurementType]:
        """Get types of available measurements for this node (async).

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of measurement type enums
        :rtype:
            `list(~ngenic.models.measurement.MeasurementType)
        """
        if not self._measurement_types:
            url = API_PATH["measurements_types"].format(
                tune_uuid=self._parent_tune_uuid, node_uuid=self.uuid()
            )
            measurements = self._parse(await self._async_get(url, invalidate_cache))
            self._measurement_types = [MeasurementType(m) for m in measurements]

        return self._measurement_types

    def measurement(
        self,
        measurement_type: MeasurementType,
        from_dt: str | None = None,
        to_dt: str | None = None,
        period: str | None = None,
        invalidate_cache: bool = False,
    ) -> Measurement | list[Measurement] | None:
        """Get measurement for a specific period.

        :param MeasurementType measurement_type:
            (required) type of measurement
        :param from_dt:
            (optional) from datetime (ISO 8601:2004)
        :param to_dt:
            (optional) to datetime (ISO 8601:2004)
        :param period:
            (optional) Divides measurement interval into periods,
            default is a single period over entire interval.
            (ISO 8601:2004 duration format)
        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            the measurement.
            if no data is available for the period, None will be returned.
        :rtype:
            `list(~ngenic.models.measurement.Measurement)`
        """
        if from_dt is None:
            url = API_PATH["measurements_latest"].format(
                tune_uuid=self._parent_tune_uuid, node_uuid=self.uuid()
            )
            url += f"?type={measurement_type.value}"
            return self._parse_new_instance(
                url, Measurement, invalidate_cache, measurement_type=measurement_type
            )
        url = API_PATH["measurements"].format(
            tune_uuid=self._parent_tune_uuid, node_uuid=self.uuid()
        )
        url += f"?type={measurement_type.value}&from={from_dt}&to={to_dt}"
        if period:
            url += f"&period={period}"
        return self._parse_new_instance(
            url, Measurement, invalidate_cache, measurement_type=measurement_type
        )

    async def async_measurement(
        self,
        measurement_type: MeasurementType,
        from_dt: str | None = None,
        to_dt: str | None = None,
        period: str | None = None,
        invalidate_cache: bool = False,
    ) -> Measurement | list[Measurement] | None:
        """Get measurement for a specific period (async).

        :param MeasurementType measurement_type:
            (required) type of measurement
        :param from_dt:
            (optional) from datetime (ISO 8601:2004)
        :param to_dt:
            (optional) to datetime (ISO 8601:2004)
        :param period:
            (optional) Divides measurement interval into periods,
            default is a single period over entire interval.
            (ISO 8601:2004 duration format)
        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            the measurement.
            if no data is available for the period, None will be returned.
        :rtype:
            `list(~ngenic.models.measurement.Measurement)`
        """
        if from_dt is None:
            url = API_PATH["measurements_latest"].format(
                tune_uuid=self._parent_tune_uuid, node_uuid=self.uuid()
            )
            url += f"?type={measurement_type.value}"
            return await self._async_parse_new_instance(
                url, Measurement, invalidate_cache, measurement_type=measurement_type
            )
        url = API_PATH["measurements"].format(
            tune_uuid=self._parent_tune_uuid, node_uuid=self.uuid()
        )
        url += f"?type={measurement_type.value}&from={from_dt}&to={to_dt}"
        if period:
            url += f"&period={period}"
        return await self._async_parse_new_instance(
            url, Measurement, invalidate_cache, measurement_type=measurement_type
        )

    def measurements(self, invalidate_cache: bool = False) -> list[Measurement]:
        """Get latest measurements for a Node.

        Usually, you can get measurements from a `NodeType.SENSOR` or `NodeType.CONTROLLER`.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of measurements (if supported by the node)
        :rtype:
            `list(~ngenic.models.measurement.Measurement)`
        """
        # get available measurement types for this node
        measurement_types = self.measurement_types(invalidate_cache)

        # remove types that doesn't support reading from latest API
        if MeasurementType.ENERGY in measurement_types:
            measurement_types.remove(MeasurementType.ENERGY)
        if MeasurementType.PRODUCED_ENERGY in measurement_types:
            measurement_types.remove(MeasurementType.PRODUCED_ENERGY)

        if len(measurement_types) == 0:
            return []

        # retrieve latest measurement for each type
        latest_measurements = list(
            self.measurement(t, None, None, None, invalidate_cache)
            for t in measurement_types
        )

        # remove None measurements (caused by measurement types returning empty response)
        return list(m for m in latest_measurements if m)

    async def async_measurements(
        self, invalidate_cache: bool = False
    ) -> list[Measurement]:
        """Get latest measurements for a Node (async).

        Usually, you can get measurements from a `NodeType.SENSOR` or `NodeType.CONTROLLER`.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of measurements (if supported by the node)
        :rtype:
            `list(~ngenic.models.measurement.Measurement)`
        """
        # get available measurement types for this node
        measurement_types = await self.async_measurement_types(invalidate_cache)

        # remove types that doesn't support reading from latest API
        if MeasurementType.ENERGY in measurement_types:
            measurement_types.remove(MeasurementType.ENERGY)
        if MeasurementType.PRODUCED_ENERGY in measurement_types:
            measurement_types.remove(MeasurementType.PRODUCED_ENERGY)

        if len(measurement_types) == 0:
            return []

        # retrieve latest measurement for each type
        return list(
            await asyncio.gather(
                *[
                    self.async_measurement(t, None, None, None, invalidate_cache)
                    for t in measurement_types
                ]
            )
        )

    def status(self, invalidate_cache: bool = False) -> NodeStatus | None:
        """Get status about this Node.

        There are no API for getting the status for a single node, so we
        will use the list API and find our node in there.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a status object or None if Node doesn't support status
        :rtype:
            `~ngenic.models.node_status.NodeStatus`
        """
        url = API_PATH["node_status"].format(tune_uuid=self._parent_tune_uuid)
        rsp_json = self._parse(self._get(url, invalidate_cache))

        for status_obj in rsp_json:
            if status_obj["nodeUuid"] == self.uuid():
                return self._new_instance(NodeStatus, status_obj, node_uuid=self.uuid())
        return None

    async def async_status(self, invalidate_cache: bool = False) -> NodeStatus | None:
        """Get status about this Node (async).

        There are no API for getting the status for a single node, so we
        will use the list API and find our node in there.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not

        :return:
            a status object or None if Node doesn't support status
        :rtype:
            `~ngenic.models.node_status.NodeStatus`
        """
        url = API_PATH["node_status"].format(tune_uuid=self._parent_tune_uuid)
        rsp_json = self._parse(await self._async_get(url, invalidate_cache))

        for status_obj in rsp_json:
            if status_obj["nodeUuid"] == self.uuid():
                return self._new_instance(NodeStatus, status_obj, node_uuid=self.uuid())
        return None
