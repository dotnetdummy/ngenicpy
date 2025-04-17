"""Mock base class for testing API responses."""

import json
from unittest import mock

from .const import API_TEST_TOKEN


class MockBase(object):
    """Mock base class for testing API responses."""

    def __init__(self, instance_class, instance_json):
        self._instance_class = instance_class
        self._instance_json = instance_json

    def single_instance(self, **kwargs):
        """Get a single instance of this mock class, without calling any APIs."""
        return self._instance_class(
            API_TEST_TOKEN, json.loads(self._instance_json), **kwargs
        )

    def multi_instance(self, **kwargs):
        """Get a list of instance of this mock class, without calling any APIs."""
        return list(
            self._instance_class(
                API_TEST_TOKEN, json.loads(self._instance_json), **kwargs
            ),
            self._instance_class(
                API_TEST_TOKEN, json.loads(self._instance_json), **kwargs
            ),
        )

    def mock_response(self):
        """Get a mock Response object for a single instance of this class."""
        return self._mock_response(content=self._instance_json)

    def mock_list_response(self):
        """Get a mock Response object for a list of instance of this class."""
        return self._mock_response(
            content=f"[{self._instance_json},{self._instance_json}]"
        )

    def _mock_response(
        self, status=200, content="{}", is_json=True, raise_for_status=None
    ):
        """Create a mock Response object that can be used to mock e.g. requests.get"""
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if is_json:
            mock_resp.json = mock.Mock(return_value=json.loads(content))
        return mock_resp
