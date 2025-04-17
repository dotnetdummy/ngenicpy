"""Exceptions for ngenicpy."""


class NgenicException(Exception):
    """Base exception class."""


class ApiException(NgenicException):
    """Exception from ngenic API."""


class ClientException(NgenicException):
    """Exception from library."""

    def __init__(self, msg: str) -> None:
        """Initialize the exception."""
        super().__init__(self, msg)
        self.msg = msg
