"""Ngenic Node Status model."""

import logging
from typing import Any

import httpx

from .base import NgenicBase

_LOGGER = logging.getLogger(__name__)


class NodeStatus(NgenicBase):
    """Ngenic API node status model."""

    def __init__(
        self, session: httpx.AsyncClient, json_data: dict[str, Any], node_uuid: str
    ) -> None:
        """Initialize the node status model."""
        self._parent_node_uuid = node_uuid

        super().__init__(session=session, json_data=json_data)

    def battery_percentage(self) -> int:
        """Get the battery percentage."""
        if self["maxBattery"] == 0:
            # not using batteries
            _LOGGER.debug("Node %s is not using batteries", self._parent_node_uuid)
            return 100

        return int((self["battery"] / self["maxBattery"]) * 100)

    def radio_signal_percentage(self) -> int:
        """Get the radio signal percentage."""
        if self["maxRadioStatus"] == 0:
            # shouldn't happen as of now (always maxRadioStatus is always 4)
            return 100

        return int((self["radioStatus"] / self["maxRadioStatus"]) * 100)
