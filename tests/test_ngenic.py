"""Test Ngenic API"""

from unittest import mock

from ngenicpy import Ngenic
from ngenicpy.models import Room, Tune

from . import UnitTest
from .const import API_TEST_TOKEN, ROOM_UUID, TUNE_UUID
from .mock_room import MockRoom
from .mock_tune import MockTune


class TestNgenic(UnitTest):
    """Test Ngenic API"""

    @mock.patch("requests.get", side_effect=MockTune().mock_response)
    def test_tunes_get(self):
        """Test get a single tune"""
        ngenic = Ngenic(token=API_TEST_TOKEN)
        tune = ngenic.tune(TUNE_UUID)

        assert isinstance(tune, Tune)
        assert tune["name"] == "Johanna Johansson"

    @mock.patch("requests.get", side_effect=MockTune().mock_list_response)
    def test_tunes_get_all(self):
        """Test get all tunes"""
        ngenic = Ngenic(token=API_TEST_TOKEN)
        tunes = ngenic.tunes()

        assert isinstance(tunes, list)
        assert all(isinstance(x, Tune) for x in tunes)

    @mock.patch("requests.get", side_effect=MockRoom().mock_response)
    def test_rooms_get(self):
        """Test get a single room"""
        tune = MockTune().single_instance()
        room = tune.room(ROOM_UUID)

        assert isinstance(room, Room)
        assert room["name"] == "Main hallway"

    @mock.patch("requests.put", side_effect=MockRoom().mock_response)
    def test_rooms_update(self):
        """Test update a single room"""
        tune = MockTune().single_instance()
        room = MockRoom().single_instance(tune=tune)
        room["name"] = "Hallway"
        room.update()

        assert isinstance(room, Room)
        assert room["name"] == "Hallway"
