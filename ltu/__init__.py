"""Declare 'ltu' namespace.

@see http://www.python.org/dev/peps/pep-0382/
"""
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
