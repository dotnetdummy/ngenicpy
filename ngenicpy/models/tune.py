"""Tune model."""

from typing import Any

import httpx

from ..const import API_PATH  # noqa: TID252
from .base import NgenicBase
from .node import Node
from .room import Room
from .setpoint_schedule import SetpointSchedule


class Tune(NgenicBase):
    """Ngenic API Tune model."""

    def __init__(self, session: httpx.AsyncClient, json_data: dict[str, Any]) -> None:
        """Initialize the tune model."""
        super().__init__(session=session, json_data=json_data)

    def uuid(self) -> str:
        """Get the tune UUID."""

        # If a tune was fetched with the list API, it contains "tuneUuid"
        # If it was fetched directly (with UUID), it contains "uuid"
        try:
            return self["tuneUuid"]
        except AttributeError:
            return super().uuid()

    def rooms(self, invalidate_cache: bool = False) -> list[Room]:
        """List all Rooms associated with a Tune.
        A Room contains an indoor sensor.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of rooms
        :rtype:
            `list(~ngenic.models.room.Room)`
        """
        url = API_PATH["rooms"].format(tune_uuid=self.uuid(), room_uuid="")
        return self._parse_new_instance(
            url, Room, invalidate_cache, tune_uuid=self.uuid()
        )

    async def async_rooms(self, invalidate_cache: bool = False) -> list[Room]:
        """List all Rooms associated with a Tune (async).
        A Room contains an indoor sensor.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of rooms
        :rtype:
            `list(~ngenic.models.room.Room)`
        """
        url = API_PATH["rooms"].format(tune_uuid=self.uuid(), room_uuid="")
        return await self._async_parse_new_instance(
            url, Room, invalidate_cache, tune_uuid=self.uuid()
        )

    def room(self, room_uuid: str, invalidate_cache: bool = False) -> Room:
        """Get data about a Room.
        A Room contains an indoor sensor.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :param str room_uuid:
            (required) room UUID
        :return:
            the room
        :rtype:
            `~ngenic.models.room.Room`
        """
        url = API_PATH["rooms"].format(tune_uuid=self.uuid(), room_uuid=room_uuid)
        return self._parse_new_instance(
            url, Room, invalidate_cache, tune_uuid=self.uuid()
        )

    async def async_room(self, room_uuid: str, invalidate_cache: bool = False) -> Room:
        """Get data about a Room (async).
        A Room contains an indoor sensor.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :param str room_uuid:
            (required) room UUID
        :return:
            the room
        :rtype:
            `~ngenic.models.room.Room`
        """
        url = API_PATH["rooms"].format(tune_uuid=self.uuid(), room_uuid=room_uuid)
        return await self._async_parse_new_instance(
            url, Room, invalidate_cache, tune_uuid=self.uuid()
        )

    def nodes(self, invalidate_cache: bool = False) -> list[Node]:
        """List all Nodes associated with a Tune.
        A Node is a logical network entity.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of nodes
        :rtype:
            `list(~ngenic.models.node.Node)`
        """
        url = API_PATH["nodes"].format(tune_uuid=self.uuid(), node_uuid="")
        return self._parse_new_instance(
            url, Node, invalidate_cache, tune_uuid=self.uuid()
        )

    async def async_nodes(self, invalidate_cache: bool = False) -> list[Node]:
        """List all Nodes associated with a Tune (async).
        A Node is a logical network entity.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of nodes
        :rtype:
            `list(~ngenic.models.node.Node)`
        """
        url = API_PATH["nodes"].format(tune_uuid=self.uuid(), node_uuid="")
        return await self._async_parse_new_instance(
            url, Node, invalidate_cache, tune_uuid=self.uuid()
        )

    def node(self, node_uuid: str, invalidate_cache: bool = False) -> Node:
        """Get data about a Node (async).
        A Node is a logical network entity.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :param str node_uuid:
            (required) node UUID
        :return:
            the node
        :rtype:
            `~ngenic.models.node.Node`
        """
        url = API_PATH["nodes"].format(tune_uuid=self.uuid(), node_uuid=node_uuid)
        return self._parse_new_instance(
            url, Node, invalidate_cache, tune_uuid=self.uuid()
        )

    async def async_node(self, node_uuid: str, invalidate_cache: bool = False) -> Node:
        """Get data about a Node (async).
        A Node is a logical network entity.

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :param str node_uuid:
            (required) node UUID
        :return:
            the node
        :rtype:
            `~ngenic.models.node.Node`
        """
        url = API_PATH["nodes"].format(tune_uuid=self.uuid(), node_uuid=node_uuid)
        return await self._async_parse_new_instance(
            url, Node, invalidate_cache, tune_uuid=self.uuid()
        )

    def setpoint_schedule(
        self, name: str, invalidate_cache: bool = False
    ) -> SetpointSchedule:
        """Fetch the setpoint schedule.

        :param str name:
            name of the setpoint schedule
        :param bool invalidate_cache:
            if the cache should be invalidated or not (default: False)
        :return:
            the setpoint schedule
        :rtype:
            `~ngenic.models.setpoint_schedule.SetPointSchedule`
        """

        url = API_PATH["setpoint_schedules"].format(tune_uuid=self.uuid())
        rsp_json = self._parse(self._get(url, invalidate_cache))

        for obj in rsp_json:
            if obj["name"] == name:
                return self._new_instance(SetpointSchedule, obj, tune_uuid=self.uuid())

        new_json = {
            "name": name,
            "autoTune": True,
            "lowestSetpoint": 12,
        }
        return self._new_instance(SetpointSchedule, new_json, tune_uuid=self.uuid())

    async def async_setpoint_schedule(
        self, name: str, invalidate_cache: bool = False
    ) -> SetpointSchedule:
        """Fetch the setpoint schedule (async).

        :param str name:
            name of the setpoint schedule
        :param bool invalidate_cache:
            if the cache should be invalidated or not (default: False)
        :return:
            the setpoint schedule
        :rtype:
            `~ngenic.models.setpoint_schedule.SetPointSchedule`
        """

        url = API_PATH["setpoint_schedules"].format(tune_uuid=self.uuid())
        rsp_json = self._parse(await self._async_get(url, invalidate_cache))

        for obj in rsp_json:
            if obj["name"] == name:
                return self._new_instance(SetpointSchedule, obj, tune_uuid=self.uuid())

        new_json = {
            "name": name,
            "autoTune": True,
            "lowestSetpoint": 12,
        }
        return self._new_instance(SetpointSchedule, new_json, tune_uuid=self.uuid())
