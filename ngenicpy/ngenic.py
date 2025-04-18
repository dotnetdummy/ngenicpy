"""This module contains the main interfaces to the API."""

import ssl

import httpx

from .const import API_PATH
from .models import NgenicBase, Tune

# 30sec for connect, 10sec elsewhere.
timeout = httpx.Timeout(10.0, connect=20.0)


def _create_local_ssl_context() -> ssl.SSLContext:
    """Create SSL context."""
    return ssl.create_default_context()


# The default SSLContext objects are created at import time
SSL_CONTEXT_LOCAL_API = _create_local_ssl_context()


class BaseClient(NgenicBase):
    """Base class for the Ngenic API client."""

    def tunes(self, invalidate_cache: bool = False):
        """Fetch all tunes

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of tunes
        :rtype:
            `list(~ngenic.models.tune.Tune)`
        """
        url = API_PATH["tunes"].format(tune_uuid="")
        return self._parse_new_instance(url, Tune, invalidate_cache)

    async def async_tunes(self, invalidate_cache: bool = False) -> list[Tune]:
        """Fetch all tunes (async)

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :return:
            a list of tunes
        :rtype:
            `list(~ngenic.models.tune.Tune)`
        """
        url = API_PATH["tunes"].format(tune_uuid="")
        return await self._async_parse_new_instance(url, Tune, invalidate_cache)

    def tune(self, tune_uuid: str, invalidate_cache: bool = False) -> Tune:
        """Fetch a single tune

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :param str tune_uuid:
            (required) tune UUID
        :return:
            the tune
        :rtype:
            `~ngenic.models.tune.Tune`
        """
        url = API_PATH["tunes"].format(tune_uuid=tune_uuid)
        return self._parse_new_instance(url, Tune, invalidate_cache)

    def async_tune(self, tune_uuid: str, invalidate_cache: bool = False) -> Tune:
        """Fetch a single tune

        :param bool invalidate_cache:
            (optional) if the cache should be invalidated or not
        :param str tune_uuid:
            (required) tune UUID
        :return:
            the tune
        :rtype:
            `~ngenic.models.tune.Tune`
        """
        url = API_PATH["tunes"].format(tune_uuid=tune_uuid)
        return self._async_parse_new_instance(url, Tune, invalidate_cache)


class Ngenic(BaseClient):
    """Ngenic API client."""

    def __init__(self, token):
        """Initialize the client.

        :param token:
            (required) OAuth2 bearer token
        """

        # this will be added to the HTTP Authorization header for each request
        self._token = token

        # this header will be added to each HTTP request
        self._auth_headers = {"Authorization": f"Bearer {self._token}"}

        session = httpx.Client(
            headers=self._auth_headers, timeout=timeout, verify=SSL_CONTEXT_LOCAL_API
        )

        # initializing this doesn't require a session or json
        super(Ngenic, self).__init__(session=session)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """Close the session if it was not created as a context manager"""
        self._session.close()


class AsyncNgenic(BaseClient):
    """Ngenic API client (async)."""

    def __init__(self, token):
        """Initialize the async client.

        :param token:
            (required) OAuth2 bearer token
        """

        # this will be added to the HTTP Authorization header for each request
        self._token = token

        # this header will be added to each HTTP request
        self._auth_headers = {"Authorization": f"Bearer {self._token}"}

        session = httpx.AsyncClient(
            headers=self._auth_headers, timeout=timeout, verify=SSL_CONTEXT_LOCAL_API
        )

        # initializing this doesn't require a session or json
        super(AsyncNgenic, self).__init__(session=session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.async_close()

    async def async_close(self):
        """Close the session if it was not created as a context manager"""
        await self._session.aclose()
