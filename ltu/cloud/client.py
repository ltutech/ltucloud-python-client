import logging
import os
import requests
#from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class CloudClient(object):
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


  def get_data(self, params={}):
    """Return appropriate HTTP POST parameters

    Args:
      params: a dictionary with service-specific parameters
    Returns:
      filtered_params to be passed to requests.
    """
    data = []
    for key, val in params.items():
      if val is not None:
        if isinstance(val, (list, tuple, set)):
          for v in val:
            data.append((key, v));
        else:
          data.append((key, val))
    return data


  def _load_image_data(self, image):
    """Make sure image is pointing to a data buffer.
    """
    if type(image) == str:
      return open(image, 'rb')
    else:
      return image


  def _post(self, service, params={}, files=None):
    """Open corresponding API service with appropriate parameters.

    Args:
      service: service name
      params: a dictionary of arguments to be passed to the service
      files: dict of file object to transfer
    Returns:
      The json response content.
    """
    data    = self.get_data(params)
    url     = self.get_url(service)
    logger.debug("Posting to '%s'" % url)
    request = requests.post(url, auth=self.auth, data=data, files=files)
    status_code = request.status_code
    answer = request.json()
    if status_code not in [200, 201]:
        raise Exception("Error while posting to %s (code: %d, msg: %s)" % (url, status_code, answer['errors']))
    return answer


  def _get(self, service, params={}):
    """Open corresponding API service with appropriate parameters.

    Args:
      service: service name
      params: a dictionary of arguments to be passed to the service
    Returns:
      The json response content.
    """
    data    = self.get_data(params)
    url     = self.get_url(service)
    logger.debug("Getting from '%s'" % url)
    request = requests.get(url, auth=self.auth, data=data)
    status_code = request.status_code
    answer = request.json()
    if status_code not in [200, 201]:
        raise Exception("Error while getting from %s (code: %d, msg: %s)" % (url, status_code, answer['errors']))
    return answer


  def _delete(self, service):
    """Open corresponding API service with appropriate parameters.

    Args:
      service: service name
    """
    url     = self.get_url(service)
    logger.debug("Deleting '%s'" % url)
    request = requests.delete(url, auth=self.auth)
    status_code = request.status_code
    if status_code not in [204]:
        raise Exception("Error while deleting %s (code: %d)" % (url, status_code))


  def search_image(self, image, project_ids=[]):
    """Image retrieval based on a image stored on disk

    Args:
      image: path to image file.
      project_ids: list of project to search into
    """
    logger.info("Search image %s into projects : %s" % (image, project_ids))
    image_buffer = self._load_image_data(image)
    return self._post("queries",
                      params={"projects": project_ids},
                      files={"image": image_buffer})


  def add_visual(self, title, name, project_id, images=[], metadata={}):
    """Create a new visual with some images
    Returns:
        The visual ID
    """
    logger.info("Adding visual: %s / %s" % (title, name))
    # create the visual
    params = {'title': title,
              'name': name
             }
    result = self._post("projects/%d/visuals/" % project_id, params=params)
    # TODO: manage existing visual
    # collect visual id
    visual_id = result['id']
    # add images
    self.add_images_to_visual(visual_id, images)
    # add meta data
    self.add_metadata_to_visual(visual_id, metadata)
    return visual_id


  def add_images_to_visual(self, visual_id, images=[]):
    """Add image fomes to an existing visual_id

    Args:
      visual_id: LTU Cloud visual id
      images: list of image files to add to the visual
    """
    for image in images:
      logger.info("Adding image %s to visual %d" % (image, visual_id))
      image_buffer = self._load_image_data(image)
      result = self._post("projects/visuals/%d/images/" % visual_id, files={'image':image_buffer})


  def add_metadata_to_visual(self, visual_id, metadata={}):
    """Add given metadata to Visual

    Args:
      visual_id: LTU Cloud visual id
      metadata: dict of metadata to add to the visual
    """
    for key, value in metadata.items():
      logger.info("Adding metadata (%s:%s) to visual %d" % (key, value, visual_id))
      result = self._post("projects/visuals/%d/metadata/" % visual_id,
                          params={'key':key, 'value':value})


  def delete_visual(self, visual_id):
    """Remove a visual from the database"""
    logger.info("Deleting visual %d" % visual_id)
    self._delete("projects/visuals/%d/" % visual_id)