"""Unit test base class for NgenicPy."""

from ngenicpy import Ngenic


class UnitTest:
    """Base class for unit tests."""

    def setup(self):
        """Setup runs before all test cases."""
        self.ngenic = Ngenic(token="dummy")
