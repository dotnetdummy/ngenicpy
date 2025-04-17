"""Tune mock class."""

from ngenicpy.models import Tune

from .mock_base import MockBase

TEST_JSON = """
{
    "isInstalled": true,
    "isNetworkConnected": true,
    "name": "Johanna Johansson",
    "priceArea": 3,
    "tuneName": "Villa Rosebud",
    "tuneUuid": "f453152b-98d9-e611-80c3-0123456789ab",
    "userName": "johanna.johansson@example.domain"
}
"""


class MockTune(MockBase):
    """Mock class for testing Tune API responses."""

    def __init__(self):
        super(MockTune, self).__init__(Tune, TEST_JSON)
