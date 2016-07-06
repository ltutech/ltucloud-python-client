"""Cloud HTTP Client.

Provide utilities to perform queries against LTU Cloud and retrieve the raw responses.
"""
import logging
import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

logger = logging.getLogger(__name__)


class CloudHTTPClient(object):
    """This class contains basic methods for accessing the API."""

    DEFAULT_QUERY_URL = "https://cloud.ltutech.com/api/v1/"

    def __init__(self, login, password, server_url=DEFAULT_QUERY_URL):
        """Constructor.

        Args:
          application_key:  authentication key provided by the application.
          server_url:       complete http url to the OnDemand server.
        """
        self.auth = (login, password)
        self.server_url = server_url.rstrip('/') + '/'

    def get_url(self, service):
        """Combine a service name and the server url to produce the service url."""
        return requests.compat.urljoin(self.server_url, service)

    def get_data(self, data={}):
        """Return appropriate HTTP POST parameters.

        Args:
          data: a dictionary with service-specific parameters
        Returns:
          filtered_params to be passed to requests.
        """
        _data = []
        for key, val in data.items():
            if val is not None:
                if isinstance(val, (list, tuple, set)):
                    for v in val:
                        _data.append((key, v))
                else:
                    _data.append((key, val))
        return _data

    def _load_file(self, file):
        """Make sure file is a tuple of a name and a data buffer."""
        if type(file) == str:
            return (os.path.basename(p=file), open(file, 'rb'))
        elif not isinstance(file, tuple):
            return ('file', file)
        else:
            return file

    def _post(self, service, data={}, files={}):
        """Open corresponding API service with appropriate parameters.

        Args:
          service: service name
          data: the request body
          files: dict of objects to be transfered. Keys must be the param name,
                 values must be tuples of (filename, file) e.g
                 {'images-image': ('image.jpg': open('/foo/bar.jpg', 'rb'))}
        Returns:
            The requests.Reponse object
        """
        url = self.get_url(service)
        logger.debug("Posting to '%s'" % url)
        headers = {}
        if files:
            for file in files.items():
                data[file[0]] = file[1]
            data.update(files)
            # requests_toolbelt MultipartEncoder prevents files from being entirely read into memory
            data = MultipartEncoder(fields=data)
            headers['Content-Type'] = data.content_type
        try:
            return requests.post(url, auth=self.auth, data=data, headers=headers)
        except Exception as e:
            return requests.Response(reason=str(e), status_code=500)

    def _get(self, service, data={}, params={}):
        """Open corresponding API service with appropriate parameters.

        Args:
          service: service name
          data: the request body
        Returns:
          The requests.Reponse object
        """
        data = self.get_data(data)
        url = self.get_url(service)
        logger.debug("Getting from '%s'" % url)
        try:
            return requests.get(url, auth=self.auth, data=data, params=params)
        except Exception as e:
            return requests.Response(reason=str(e), status_code=500)

    def _delete(self, service):
        """Open corresponding API service with appropriate parameters.

        Args:
          service: service name
        Returns:
          The requests.Reponse object
        """
        url = self.get_url(service)
        logger.debug("Deleting '%s'" % url)
        try:
            return requests.delete(url, auth=self.auth)
        except Exception as e:
            return requests.Response(reason=str(e), status_code=500)

    def search_image(self, image, project_ids=[], **kwargs):
        """Image retrieval based on a image stored on disk.

        Args:
          image: path to image file.
          project_ids: list of project to search into
          **kwargs: any additional kwarg will be added to the request body.
        Returns:
          The requests.Reponse object
        """
        logger.info("Search image %s into projects : %s" % (image, project_ids))
        image_buffer = self._load_file(image)
        data = {}
        if project_ids:
            data = {"projects": project_ids}
        # add any other keyword argument
        data.update(kwargs)
        return self._post("queries",
                          data=data,
                          files={"image": image_buffer})

    def get_visual(self, visual_id):
        """Retrieve a visual from its id."""
        logger.info("Getting visual with id {}".format(visual_id))
        return self._get("projects/visuals/{}".format(visual_id))

    def get_visuals(self, project_id=None, **kwargs):
        """Retrieve visuals.

        Args:
            project_id: if provided, get that project's visuals otherwise get all accessible
                        projects visuals.
            **kwargs: any additional kwarg will be added to the URL query string (e.g: limit=10)
        Returns:
            The raw Cloud response.
        """
        if project_id:
            log_message = "Getting project {} visuals.".format(project_id)
            url = "projects/{}/visuals/".format(project_id)
        else:
            log_message = "Getting visuals."
            url = "projects/visuals/"
        logger.info(log_message)
        return self._get(url, params=kwargs)

    def add_visual(self, title, project_id, name=None, image=None, metadata={}, **kwargs):
        """Create a new visual.

        Returns:
          The requests.Reponse object
        """
        logger.info("Adding visual: %s / %s" % (title, name))
        # create the visual
        data = {'title': title,
                'name': name}
        # add the metadatas
        data.update(self._format_metadata_multipart(metadata))
        # add any other keyword argument
        data.update(kwargs)
        if image:
            files = {'images-image': self._load_file(image)}
        else:
            files = {}
        # TODO: manage existing visual
        return self._post("projects/%d/visuals/" % int(project_id), data=data,
                          files=files)

    def _format_metadata_multipart(self, metadatas):
        """Format metadata to be upload as multipart content."""
        metas = {}
        for idx, meta in enumerate(metadatas.items()):
            metas['metadata-{}-key'.format(idx)] = meta[0]
            metas['metadata-{}-value'.format(idx)] = meta[1]
        return metas

    def _format_metadata_json(self, metadatas):
        """Format metadata to be sent as json content."""
        metas = {}
        for meta in metadatas.items():
            metas['key'] = meta[0]
            metas['value'] = meta[1]
        return metas

    def add_images_to_visual(self, visual_id, images=[]):
        """Add image fomes to an existing visual_id.

        Args:
          visual_id: LTU Cloud visual id
          images: list of image files to add to the visual
        Returns:
          The requests.Reponse object
        """
        for image in images:
            logger.info("Adding image %s to visual %d" % (image, visual_id))
            image_buffer = self._load_file(image)
            return self._post("projects/visuals/%d/images/" % visual_id,
                              files={'image': image_buffer})

    def add_metadata_to_visual(self, visual_id, metadata={}):
        """Add given metadata to Visual.

        Args:
          visual_id: LTU Cloud visual id
          metadata: dict of metadata to add to the visual
        Returns:
          The requests.Reponse object
        """
        logger.info("Adding metadata %s to visual %d" % (metadata, visual_id))
        return self._post("projects/visuals/%d/metadata/" % visual_id,
                          data=self._format_metadata_json(metadata))

    def delete_visual(self, visual_id):
        """Remove a visual.

        Returns:
          The requests.Reponse object
        """
        logger.info("Deleting visual %d" % visual_id)
        return self._delete("projects/visuals/%d/" % visual_id)

    def get_query(self, query_id):
        """Retrieve a query.

        Args:
            query_id: the id of the query to retrieve.
        Returns:
            The raw Cloud response.
        """
        logger.info("Getting query with id {}".format(query_id))
        return self._get("queries/{}".format(query_id))

    def get_queries(self, **kwargs):
        """Retrieve queries.

        Args:
            **kwargs: any kwarg will be added to the URL query string (e.g: limit=10)
        Returns:
            The raw Cloud response.
        """
        logger.info("Getting queries")
        return self._get("queries/", params=kwargs)
