==================================================
====== LTU Cloud - Python Client ======
==================================================

==============================================
ABOUT THIS CLIENT
==============================================

Jastec France is a company that provides image recognition as a service.
This Python module is a client that allows you to access the HTTP API to
perform image recognition tasks. For more information on image recognition,
please visit http://www.jastec.fr.


Note that this client cannot be used without a valid LTU Cloud account.
Please contact our sales department to get your account today
(sales@jastec.fr) or create an evaluation account Online
(http://www.jastec.fr/get_started/).

==============================================
INSTALL
==============================================

The client comes in the form of a multiplatform python package. Although the
package has been tested on linux platforms only, it should run fine under
Windows.

Package can be installed along with dependencies by running:

  python setup.py install

Note that python 2.6.+ or later is required. Your python version can be
obtained by running:

  python --version

==============================================
BASIC USAGE
==============================================

Adding a visual with images and metadata:

  from client import CloudClient
  client = CloudClient(MY_LOGIN, MY_PASSWORD)
  image_files = [image_path1]
  metadata = {'data': 'None'}
  visual_id = client.add_visual("Visual Title",
                                "Visual Name",
                                MY_PROJECT_ID,
                                images=image_files,
                                metadata=metadata)

Delete a visual:

  from client import CloudClient
  client = CloudClient(MY_LOGIN, MY_PASSWORD)
  visual_id = ...
  client.delete_visual(visual_id)


Perform an image search:

  from client import CloudClient
  client = CloudClient(MY_LOGIN, MY_PASSWORD)
  result = client.search_image(image_path)
  print(result)

==============================================
ADVANCED USAGE
==============================================

For advanced usage, please consult the docstrings for each function.

==============================================
LICENSE
==============================================

This software is licensed under the terms of the Apache License 2.0. In
particular, you are free to distribute it, modify it and to distribute modified
versions as long as you include the attached NOTICE file with your software.
Read the attached LICENSE file for more information.

===============================================
CREDITS & USAGE:
===============================================

Feel free to use any of the resources provided in this client.

EMAIL: support@jastec.fr