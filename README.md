# LTU Cloud - Python Client

# About this client

Jastec France is a company that provides image recognition as a service.
This Python module is a client that allows you to access the HTTP API to
perform image recognition tasks. For more information on image recognition,
please visit [http://www.jastec.fr](http://www.jastec.fr).


Note that this client cannot be used without a valid LTU Cloud account.
Please contact our sales department to get your account today
(sales@jastec.fr) or [create an evaluation account Online]
(http://www.jastec.fr/get_started/).


# Install

The client comes in the form of a multiplatform python package. Although the
package has been tested on linux platforms only, it should run fine under
Windows.

Note that python 2.6.+ or later is required.
To know if python is already installed or to check the version use the following command:
```bash
python --version
```

In first, install virtualenv  by typing the folling command in a terminal:
```bash
sudo apt-get install virtualenv

```

Then, create and activate your dev environment in the project folder.
```bash
cd ltucloud-python-client
virtualenv env
source env/bin/activate
```

The package can be installed along with dependencies by running:
```bash
python setup.py install
```


# Basic usage

### Adding a visual with images and metadata:

```python
from ltu.cloud.client import CloudClient

client = CloudClient(MY_LOGIN, MY_PASSWORD)
image_files = [image_path1]
metadata = {'data': 'None'}
visual_id = client.add_visual("Visual Title",
                              "Visual Name",
                              MY_PROJECT_ID,
                              images=image_files,
                              metadata=metadata)
```

### Delete a visual:
```python
from ltu.cloud.client import CloudClient

client = CloudClient(MY_LOGIN, MY_PASSWORD)
visual_id = ...
client.delete_visual(visual_id)
```

### Perform an image search:

```python
from ltu.cloud.client import CloudClient
client = CloudClient(MY_LOGIN, MY_PASSWORD)
result = client.search_image(image_path)
print(result)
```


# Advanced usage

For advanced usage, please consult the docstrings for each function.


# Licence

This software is licensed under the terms of the Apache License 2.0. In
particular, you are free to distribute it, modify it and to distribute modified
versions as long as you include the attached NOTICE file with your software.
Read the attached LICENSE file for more information.


# Credits & usage:

Feel free to use any of the resources provided in this client.

email: support@jastec.fr
