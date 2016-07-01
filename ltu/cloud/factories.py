"""LTU Cloud factories.

This module provides some factories to quickly create LTU Cloud objects.
"""
import factory
from faker import Factory as FakerFactory

from ltu.cloud import models

# create a fake factory
faker = FakerFactory.create()


class ResourceCommonFactory(factory.Factory):
    """Create resource common objects."""

    class Meta:
        """Setup the factory model."""

        model = models.ResourceCommon

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda _: faker.word())
    created_at = factory.LazyAttribute(lambda _: faker.date_time())
    updated_at = factory.LazyAttribute(lambda _: faker.date_time())


class LinksFactory(factory.Factory):
    """Create LTU Cloud links objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Links

    images = factory.LazyAttribute(lambda _: faker.url())
    metadata = factory.LazyAttribute(lambda _: faker.url())
    project = factory.LazyAttribute(lambda _: faker.url())
    self = factory.LazyAttribute(lambda _: faker.url())


class MediaFactory(factory.Factory):
    """Create LTU Cloud media objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Media

    image = factory.LazyAttribute(lambda _: faker.image_url())
    thumbnail = factory.LazyAttribute(lambda _: faker.image_url())


class ImageFactory(ResourceCommonFactory):
    """Create LTU Cloud image objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Image

    _links = factory.SubFactory(LinksFactory)
    _media = factory.SubFactory(MediaFactory)
    image_md5 = factory.LazyAttribute(lambda _: faker.md5(raw_output=False))
    source = factory.LazyAttribute(lambda _: faker.word())


class MatchedImageFactory(ImageFactory):
    """Create LTU Cloud MatchedImage objects."""

    class Meta:
        """Setup the factory model."""

        model = models.MatchedImage

    score = factory.LazyAttribute(lambda _: faker.pyfloat(left_digits=3, right_digits=2,
                                                          positive=True))


class MetadataFactory(ResourceCommonFactory):
    """Create LTU Cloud metadata objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Metadata

    _links = factory.SubFactory(LinksFactory)
    key = factory.LazyAttribute(lambda _: faker.word())
    ordering = factory.Sequence(lambda n: n)
    value = factory.LazyAttribute(lambda _: faker.word())


class VisualFactory(ResourceCommonFactory):
    """Create LTU Cloud visual objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Visual

        # the following attributes won't be passed to the model class. They're just used as switches
        # or to compute other attributes
        exclude = ("nb_images", "nb_metadatas")

    _links = factory.SubFactory(LinksFactory)
    _media = factory.SubFactory(MediaFactory)
    nb_images = 1  # number of images to associate to this visual
    title = factory.LazyAttribute(lambda _: faker.word())
    project_id = factory.LazyAttribute(lambda _: faker.pyint())
    match_count = factory.LazyAttribute(lambda _: faker.pyint())
    nb_metadatas = 1  # number of metadatas to associate to this visual
    cover_id = factory.LazyAttribute(lambda _: faker.pyint())

    @factory.lazy_attribute
    def images(self):
        """Create images."""
        images = []
        if self.nb_images:
            images = ImageFactory.create_batch(size=self.nb_images)
        return images

    @factory.lazy_attribute
    def metadata(self):
        """Create metadatas."""
        metadatas = []
        if self.nb_metadatas:
            MetadataFactory.create_batch(size=self.nb_metadatas)
        return metadatas


class MatchedVisualFactory(VisualFactory):
    """Create LTU Cloud MatchedVisual objects."""

    class Meta:
        """Setup the factory model."""

        model = models.MatchedVisual
        # remove Visual only attributes
        exclude = ("cover_id", "_media", "images")

    match_count = factory.LazyAttribute(lambda _: faker.pyint())

    @factory.lazy_attribute
    def matched_images(self):
        """Create matched_images."""
        matched_images = []
        if self.nb_images:
            matched_images = MatchedImageFactory.create_batch(size=self.nb_images)
        return matched_images


class MatchFactory(VisualFactory):
    """Create LTU Cloud Match objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Match

    id = factory.Sequence(lambda n: n)
    nb_matched_images = factory.LazyAttribute(lambda _: faker.pyint())
    score = score = factory.LazyAttribute(lambda _: faker.pyfloat(left_digits=3, right_digits=2,
                                                                  positive=True))
    _links = factory.SubFactory(LinksFactory)
    matched_visual = factory.SubFactory(MatchedVisualFactory)


class QueryFactory(ResourceCommonFactory):
    """Create LTU Cloud Query objects."""

    class Meta:
        """Setup the factory model."""

        model = models.Query
        exclude = ("nb_matches", )

    _links = factory.SubFactory(LinksFactory)
    _media = factory.SubFactory(MediaFactory)
    nb_matches = 1  # number of matches to associate to this visual
    source = factory.LazyAttribute(lambda _: faker.word())
    source_description = factory.LazyAttribute(lambda _: faker.sentence(nb_words=6,
                                                                        variable_nb_words=True))

    @factory.lazy_attribute
    def matches(self):
        """Create matches."""
        matches = []
        if self.nb_matches:
            matches = MatchFactory.create_batch(size=self.nb_matches)
        return matches
