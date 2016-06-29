import logging
import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

logger = logging.getLogger(__name__)


class CloudHTTPClient(object):
    """This class contains basic methods for accessing the API.
    """
    DEFAULT_QUERY_URL = "https://cloud.ltutech.com/api/v1/"

    def __init__(self, login, password, server_url=DEFAULT_QUERY_URL):
        """Constructor
        Args:
          application_key:  authentication key provided by the application.
          server_url:       complete http url to the OnDemand server.
        """
        self.auth = (login, password)
        self.server_url = server_url

    def get_url(self, service):
        """Combine a service name and the server url to produce the service url.
        """
        return requests.compat.urljoin(self.server_url, service)

    def get_data(self, data={}):
        """Return appropriate HTTP POST parameters

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
          The json response content.
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
        request = requests.post(url, auth=self.auth, data=data, headers=headers)
        status_code = request.status_code
        answer = request.json()
        if status_code not in [200, 201]:
            raise Exception("Error while posting to %s (code: %d, msg: %s)" %
                            (url, status_code, answer['errors']))
        return answer

    def _get(self, service, data={}):
        """Open corresponding API service with appropriate parameters.

        Args:
          service: service name
          data: the request body
        Returns:
          The json response content.
        """
        data = self.get_data(data)
        url = self.get_url(service)
        logger.debug("Getting from '%s'" % url)
        request = requests.get(url, auth=self.auth, data=data)
        status_code = request.status_code
        answer = request.json()
        if status_code not in [200, 201]:
            raise Exception("Error while getting from %s (code: %d, msg: %s)" %
                            (url, status_code, answer['errors']))
        return answer

    def _delete(self, service):
        """Open corresponding API service with appropriate parameters.

        Args:
          service: service name
        """
        url = self.get_url(service)
        logger.debug("Deleting '%s'" % url)
        request = requests.delete(url, auth=self.auth)
        status_code = request.status_code
        if status_code not in [204]:
            raise Exception("Error while deleting %s (code: %d)" %
                            (url, status_code))

    def search_image(self, image, project_ids=[]):
        """Image retrieval based on a image stored on disk

        Args:
          image: path to image file.
          project_ids: list of project to search into
        """
        logger.info("Search image %s into projects : %s" % (image, project_ids))
        image_buffer = self._load_file(image)
        data = {}
        if project_ids:
            data = {"projects": project_ids}
        return self._post("queries",
                          data=data,
                          files={"image": image_buffer})

    def add_visual(self, title, name, project_id, image=None, metadata={}):
        """Create a new visual.

        Returns:
            The visual ID
        """
        logger.info("Adding visual: %s / %s" % (title, name))
        # create the visual
        data = {'title': title,
                'name': name}
        # add the metadatas
        data.update(self._format_metadata_multipart(metadata))
        if image:
            files = {'images-image': self._load_file(image)}
        else:
            files = {}
        result = self._post("projects/%d/visuals/" % project_id, data=data,
                            files=files)
        # TODO: manage existing visual
        return result['id']

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
        """Add image fomes to an existing visual_id

        Args:
          visual_id: LTU Cloud visual id
          images: list of image files to add to the visual
        """
        for image in images:
            logger.info("Adding image %s to visual %d" % (image, visual_id))
            image_buffer = self._load_file(image)
            self._post("projects/visuals/%d/images/" % visual_id,
                       files={'image': image_buffer})

    def add_metadata_to_visual(self, visual_id, metadata={}):
        """Add given metadata to Visual

        Args:
          visual_id: LTU Cloud visual id
          metadata: dict of metadata to add to the visual
        """
        logger.info("Adding metadata %s to visual %d" % (metadata, visual_id))
        self._post("projects/visuals/%d/metadata/" % visual_id,
                   data=self._format_metadata_json(metadata))

    def delete_visual(self, visual_id):
        """Remove a visual from the database"""
        logger.info("Deleting visual %d" % visual_id)
        self._delete("projects/visuals/%d/" % visual_id)
