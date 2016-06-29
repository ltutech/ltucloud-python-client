"""LTU Cloud API client.

Provide utilities to perform queries against LTU Cloud.
It wraps a CloudHTTPClient and deserializes its responses into objects.
"""
import logging

from ltu.cloud.httpclient import CloudHTTPClient
from ltu.cloud.serializers import SearchQuerySerializer, VisualSerializer


logger = logging.getLogger(__name__)


class CloudException(Exception):
    """Dummy class to cast an Exception into a CloudException."""

    pass


class CloudSerializationException(Exception):
    """Dummy class to cast an Exception into a CloudSerializationException."""

    pass


class CloudClient(object):
    """A python LTU Cloud API client."""

    def __init__(self, login, password, server_url=CloudHTTPClient.DEFAULT_QUERY_URL):
        """Initialize a CloudClient."""
        self.cloud_http_client = CloudHTTPClient(login=login, password=password,
                                                 server_url=server_url)

    def _check_response_status(self, response, expected_status):
        if response.status_code != expected_status:
            if response.reason:
                error_message = response.reason
            else:
                error_message = "Internal server error."
            raise CloudException(error_message)
        else:
            return response

    def _deserialize(self, data, serializer):
        obj, errors = serializer().load(data)
        if errors:
            raise CloudSerializationException(str(errors))
        else:
            return obj

    def search_image(self, image, project_ids=[]):
        """Search an image within the given project ids.

        If no project_ids are given, search among all account accessible projects.
        """
        cloud_response = self.cloud_http_client.search_image(image=image, project_ids=project_ids)
        cloud_response_json = self._check_response_status(cloud_response, 201).json()
        return self._deserialize(cloud_response_json, SearchQuerySerializer)

    def add_visual(self, title, name, project_id, image=None, metadata={}):
        """Create a new visual.

        Return the Cloud response as a models.Visual object.
        """
        cloud_response = self.cloud_http_client.add_visual(
                                title=title, name=name, project_id=project_id, image=image,
                                metadata=metadata)
        cloud_response_json = self._check_response_status(cloud_response, 201).json()
        return self._deserialize(cloud_response_json, VisualSerializer)
