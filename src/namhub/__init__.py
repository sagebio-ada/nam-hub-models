"""nam-hub-models.

A repository containing data models for NAMHub curation
"""

try:
    from namhub._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
