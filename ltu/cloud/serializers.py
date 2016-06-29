"""LTU Cloud object's serializers.

Provide classes for converting LTU Cloud objects to and from native Python datatypes.
"""
from marshmallow import fields, post_load, Schema

from ltu.cloud import models


class ResourceCommonSerializer(Schema):
    """Serialize resource common attributes."""

    id = fields.Int()
    name = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime(required=False, allow_none=True)

    @post_load
    def make_object(self, data):
        """Create a resource from serialized data."""
        return models.ResourceCommon(**data)


class LinksSerializer(Schema):
    """Serialize LTU Cloud _links."""

    images = fields.Url(required=False, allow_none=True)
    metadata = fields.Url(required=False, allow_none=True)
    project = fields.Url(required=False, allow_none=True)
    self = fields.Url()

    @post_load
    def make_object(self, data):
        """Create a links from serialized data."""
        return models.Links(**data)


class MediaSerializer(Schema):
    """Serialize LTU Cloud _media."""

    image = fields.Url()
    thumbnail = fields.Url()

    @post_load
    def make_object(self, data):
        """Create a media from serialized data."""
        return models.Media(**data)


class ImageSerializer(ResourceCommonSerializer):
    """Serialize LTU Cloud image."""

    _links = fields.Nested(LinksSerializer)
    _media = fields.Nested(MediaSerializer)
    image_md5 = fields.Str(required=False)
    source = fields.Str(required=False)

    @post_load
    def make_object(self, data):
        """Create an image from serialized data."""
        return models.Image(**data)


class MatchedImageSerializer(ImageSerializer):
    """Serialize LTU Cloud MatchedImage."""

    score = fields.Float()

    @post_load
    def make_object(self, data):
        """Create a MatchedImage from serialized data."""
        return models.MatchedImage(**data)


class MetadataSerializer(ResourceCommonSerializer):
    """Serialize LTU Cloud metadata."""

    _links = fields.Nested(LinksSerializer)
    key = fields.Str()
    ordering = fields.Int()
    value = fields.Str()

    @post_load
    def make_object(self, data):
        """Create a metadata from serialized data."""
        return models.Metadata(**data)


class VisualSerializer(ResourceCommonSerializer):
    """Serialize LTU Cloud visual."""

    _links = fields.Nested(LinksSerializer)
    _media = fields.Nested(MediaSerializer)
    images = fields.Nested(ImageSerializer, many=True)
    title = fields.Str()
    project_id = fields.Int()
    match_count = fields.Int()
    metadata = fields.Nested(MetadataSerializer, many=True)
    cover_id = fields.Int(allow_none=True)

    @post_load
    def make_object(self, data):
        """Create a visual from serialized data."""
        return models.Visual(**data)


class MatchedVisualSerializer(VisualSerializer):
    """Serialize LTU Cloud MatchedVisual."""

    match_count = fields.Int()
    matched_images = fields.Nested(MatchedImageSerializer, many=True)

    @post_load
    def make_object(self, data):
        """Create a MatchedVisual from serialized data."""
        return models.MatchedVisual(**data)


class MatchSerializer(VisualSerializer):
    """Serialize LTU Cloud Match."""

    id = fields.Int()
    nb_matched_images = fields.Int()
    score = fields.Float()
    _links = fields.Nested(LinksSerializer)
    matched_visual = fields.Nested(MatchedVisualSerializer)

    @post_load
    def make_object(self, data):
        """Create a Match from serialized data."""
        return models.Match(**data)


class SearchQuerySerializer(ResourceCommonSerializer):
    """Serialize LTU Cloud SearchQuery."""

    _links = fields.Nested(LinksSerializer)
    _media = fields.Nested(MediaSerializer)
    matches = fields.Nested(MatchSerializer, many=True)

    @post_load
    def make_object(self, data):
        """Create a SearchQuery from serialized data."""
        return models.SearchQuery(**data)
