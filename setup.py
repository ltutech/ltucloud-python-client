#!/usr/bin/env python
from setuptools import setup

VERSION = "1.0"
DESCRIPTION = "LTU Cloud API Python client."

PARAMETERS = {
    'name': 'ltucloud-python-client',
    'description': DESCRIPTION,
    'packages': [
        'ltu.cloud',
        'ltu'
    ],
    'namespace_packages': ['ltu'],
    'package_dir': {
        'ltu.cloud': 'ltu/cloud',
        'ltu': 'ltu'
    },
    'install_requires': [
        'requests>=2.10.0, <3.0',
        'requests-toolbelt>=0.6.2, <1.0'
        ],
    'author': "Jastec France",
    'author_email': "support@jastec.fr",
    'maintainer': "Jastec France",
    'maintainer_email': "support@jastec.fr",
    'license': "LICENSE",
    'version': VERSION,
}


if __name__ == "__main__":
    setup(**PARAMETERS)
