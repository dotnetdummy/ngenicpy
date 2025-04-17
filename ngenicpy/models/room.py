"""Room model for Ngenic Tune API."""

from typing import Any

import httpx

from ..const import API_PATH  # noqa: TID252
from .base import NgenicBase


class Room(NgenicBase):
    """Ngenic API room model."""

    def __init__(
        self, session: httpx.AsyncClient, json_data: dict[str, Any], tune_uuid: str
    ) -> None:
        """Initialize the room model."""
        self._parent_tune_uuid = tune_uuid

        super().__init__(session=session, json_data=json_data)

    def update(self) -> None:
        """Update this room with its current values."""

        url = API_PATH["rooms"].format(
            tune_uuid=self._parent_tune_uuid, room_uuid=self.uuid()
        )
        self._put(url, data=self.json())

    async def async_update(self) -> None:
        """Update this room with its current values (async)."""

        url = API_PATH["rooms"].format(
            tune_uuid=self._parent_tune_uuid, room_uuid=self.uuid()
        )
        await self._async_put(url, data=self.json())
