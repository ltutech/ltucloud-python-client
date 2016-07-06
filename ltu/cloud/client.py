"""LTU Cloud API client.

Provide utilities to perform queries against LTU Cloud.
It wraps a CloudHTTPClient and deserializes its responses into objects.
"""
import logging

from ltu.cloud.httpclient import CloudHTTPClient
from ltu.cloud.serializers import QuerySerializer, VisualSerializer


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
            error_message = response.content or response.reason or "Internal server error."
            raise CloudException(error_message)
        else:
            return response

    def _deserialize(self, data, serializer, many=False):
        obj, errors = serializer(many=many).load(data)
        if errors:
            raise CloudSerializationException(str(errors))
        else:
            return obj

    def search_image(self, image, project_ids=[]):
        """Search an image within the given project ids.

        Args:
            image: either a filepath or a tuple(name, bytes).
            project_ids: a list of project ids to search the image in. If no project_ids is
                         provided, search among all account accessible projects.
        Returns:
            the resulting Query object.
        Raises:
            CloudException: if the underlying cloud query went wrong.
            CloudSerializationException: if an error occurs when deserializing the cloud response.
        """
        cloud_response = self.cloud_http_client.search_image(image=image, project_ids=project_ids)
        cloud_response_json = self._check_response_status(cloud_response, 201).json()
        return self._deserialize(cloud_response_json, QuerySerializer)

    def add_visual(self, title, project_id, name=None, image=None, metadata={}, **kwargs):
        """Create a new visual.

        Args:
            title: the title of the visual to create.
            name: the name of the visual to create.
            project_id: the id of the project to create the visual in.
        Returns:
            the created visual
        Raises:
            CloudException: if the underlying cloud query went wrong.
            CloudSerializationException: if an error occurs when deserializing the cloud response.
        """
        cloud_response = self.cloud_http_client.add_visual(
                                title=title, name=name, project_id=project_id, image=image,
                                metadata=metadata, **kwargs)
        cloud_response_json = self._check_response_status(cloud_response, 201).json()
        return self._deserialize(cloud_response_json, VisualSerializer)

    def get_visual(self, visual_id):
        """Retrieve a visual from its id.

        Args:
            visual_id: the id of the visual to look for.
        Returns:
            the visual
        Raises:
            CloudException: if the underlying cloud query went wrong.
            CloudSerializationException: if an error occurs when deserializing the cloud response.
        """
        cloud_response = self.cloud_http_client.get_visual(visual_id=visual_id)
        cloud_response_json = self._check_response_status(cloud_response, 200).json()
        return self._deserialize(cloud_response_json, VisualSerializer)

    def get_visuals(self, project_id=None, **kwargs):
        """Retrieve visuals.

        Args:
            project_id: if provided, get that project's visuals otherwise get all accessible
                        projects visuals.
            **kwargs: any additional kwarg will be added to the URL query string (e.g: limit=10)
        Returns:
            the visuals
        Raises:
            CloudException: if the underlying cloud query went wrong.
            CloudSerializationException: if an error occurs when deserializing the cloud response.
        """
        cloud_response = self.cloud_http_client.get_visuals(project_id=project_id, **kwargs)
        cloud_response_json = self._check_response_status(cloud_response, 200).json()
        return self._deserialize(cloud_response_json.get('results', []), VisualSerializer,
                                 many=True)

    def get_query(self, query_id):
        """Retrieve a query from its id.

        Args:
            query_id: the id of the visual to look for.
        Returns:
            the query
        Raises:
            CloudException: if the underlying cloud query went wrong.
            CloudSerializationException: if an error occurs when deserializing the cloud response.
        """
        cloud_response = self.cloud_http_client.get_query(query_id=query_id)
        cloud_response_json = self._check_response_status(cloud_response, 200).json()
        return self._deserialize(cloud_response_json, QuerySerializer)

    def get_queries(self, **kwargs):
        """Retrieve queries.

        Args:
            **kwargs: any kwarg will be added to the URL query string (e.g: limit=10)
        Returns:
            the queries
        Raises:
            CloudException: if the underlying cloud query went wrong.
            CloudSerializationException: if an error occurs when deserializing the cloud response.
        """
        cloud_response = self.cloud_http_client.get_queries(**kwargs)
        cloud_response_json = self._check_response_status(cloud_response, 200).json()
        return self._deserialize(cloud_response_json.get('results', []), QuerySerializer,
                                 many=True)
