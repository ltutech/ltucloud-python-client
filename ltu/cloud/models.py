"""LTU Cloud objects."""


class ResourceCommon(object):
    """Hold common resources fields."""

    def __init__(self, id=None, name=None, created_at=None, updated_at=None, **kwargs):
        """Init the fields."""
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """String representation of a ResourceCommon."""
        return "id: {}, name: {}".format(self.id, self.name)


class Links(object):
    """Represent LTU Cloud _links.

    Each LTU Cloud 'object' has a _links attribute containing some useful links.
    """

    def __init__(this, images=None, metadata=None, project=None, self=None, **kwargs):  # noqa
        """Init the fields.

        The LTU Cloud _links 'object' has a self attribute. This is why we use this here.
        """
        this.images = images
        this.metadata = metadata
        this.project = project
        this.self = self

    def __str__(this):  # noqa
        """String representation of a Links."""
        return "self: {}, images: {}, metadata: {}, project: {}".format(this.self, this.images,
                                                                        this.metadata, this.project)


class Media(object):
    """Represent LTU Cloud _media."""

    def __init__(self, image=None, thumbnail=None, *args, **kwargs):
        """Init the fields."""
        self.image = image
        self.thumbnail = thumbnail

    def __str__(self):
        """String representation of a Media."""
        return "image: {}, thumbnail: {}".format(self.image, self.thumbnail)


class Image(ResourceCommon):
    """Represent LTU Cloud image."""

    def __init__(self, _links=None, _media=None, image_md5=None, source=None, **kwargs):
        """Init the fields."""
        super(Image, self).__init__(**kwargs)
        self._links = _links
        self._media = _media
        self.image_md5 = image_md5
        self.source = source

    def __str__(self):
        """String representation of an Image."""
        return "{}, _links: {}, _media: {}, image_md5: {}, source: {}".format(
                super(Image, self).__str__(), self._links, self._media, self.image_md5, self.source)


class MatchedImage(Image):
    """A MatchedImage is an Image of a MatchedVisual.

    Basically it's an Image with an extra score and result_info attribute.
    """

    def __init__(self, score, **kwargs):
        """Init fields."""
        super(MatchedImage, self).__init__(**kwargs)
        self.score = score
        # TODO(jpiron): handle result_info

    def __str__(self):
        """String representation of an MatchedImage."""
        return "{}, score: {}".format(super(MatchedImage, self).__str__(), self.score)


class Metadata(ResourceCommon):
    """Represent LTU Cloud metatata."""

    def __init__(self, key, ordering, value, _links=None, **kwargs):
        """Init the fields."""
        super(Metadata, self).__init__(**kwargs)
        self._links = _links
        self.key = key
        self.ordering = ordering
        self.value = value

    def __str__(self):
        """String representation of a Metadata."""
        return "{}, _links: {}, key: {}, ordering: {}, value: {}".format(
                super(Metadata, self).__str__(), self._links, self.key, self.ordering, self.value)


class Visual(ResourceCommon):
    """Represent LTU Cloud _media."""

    def __init__(self, _links=None, _media=None, images=[], title=None, project_id=None,
                 match_count=None, metadata=[], cover_id=None, **kwargs):
        """Init the fields.

        Metadata is in singular form because it is like this in LTU Cloud but it needs to be a list
        of metadata.
        """
        super(Visual, self).__init__(**kwargs)
        self._links = _links
        self._media = _media
        self.images = images
        self.title = title
        self.project_id = project_id
        self.match_count = match_count
        self.metadata = metadata
        self.cover_id = cover_id


class MatchedVisual(Visual):
    """A MatchedVisual is basically a Visual with some more and less attributes.

    Compared to a Visual, a MatchedVisual has:
        - a match_count attribute
        - a matched_images attribute. It replaces the Visual images attribute.
        - no _media attribute
        - no cover_id attribute
    """

    def __init__(self, match_count=0, matched_images=[], **kwargs):
        """Init fields."""
        super(MatchedVisual, self).__init__(**kwargs)
        self.match_count = match_count
        self.matched_images = matched_images
        del self.cover_id
        del self._media

    def __getattribute__(self, name):
        """__getattribute__ override.

        To access a MatchedVisual images the same way as for a Visual.
        """
        if name == 'images':
            return self.matched_images
        else:
            return super(MatchedVisual, self).__getattribute__(name)


class Match(object):
    """A Match is a MatchedVisual wrapper.

    It encapsulates a MatchedVisual and add some attributes.
    """

    def __init__(self, id, nb_matched_images=0, score=0, _links=None, matched_visual=None,
                 **kwargs):
        """Init fields."""
        self.id = id
        self.nb_matched_images = nb_matched_images
        self.score = score
        self._links = _links
        self.matched_visual = matched_visual


class Query(ResourceCommon):
    """Represent LTU Cloud query."""

    def __init__(self, _links=None, _media=None, matches=[], source=None, source_description=None,
                 **kwargs):
        """Init fields."""
        super(Query, self).__init__(**kwargs)
        self._links = _links
        self._media = _media
        self.matches = matches
        self.source = source
        self.source_description = source_description
