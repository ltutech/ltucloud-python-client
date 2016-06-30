"""LTU Cloud factories.

This module provides some factories to quickly create LTU Cloud objects.
"""
import factory
from faker import Factory as FakerFactory

from .models import Image, Links, Media, Metadata, ResourceCommon, Visual

# create a fake factory
faker = FakerFactory.create()


class ResourceCommonFactory(factory.Factory):
    """Create resource common objects."""

    class Meta:
        """Setup the factory model."""

        model = ResourceCommon

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda _: faker.words(nb=1))
    created_at = factory.LazyAttribute(lambda _: faker.date_time())
    updated_at = factory.LazyAttribute(lambda _: faker.date_time())


class LinksFactory(factory.Factory):
    """Create LTU Cloud links objects."""

    class Meta:
        """Setup the factory model."""

        model = Links

    images = factory.LazyAttribute(lambda _: faker.url())
    metadata = factory.LazyAttribute(lambda _: faker.url())
    project = factory.LazyAttribute(lambda _: faker.url())
    self = factory.LazyAttribute(lambda _: faker.url())


class MediaFactory(factory.Factory):
    """Create LTU Cloud media objects."""

    class Meta:
        """Setup the factory model."""

        model = Media

    image = factory.LazyAttribute(lambda _: faker.image_url())
    thumbnail = factory.LazyAttribute(lambda _: faker.image_url())


class ImageFactory(ResourceCommonFactory):
    """Create LTU Cloud image objects."""

    class Meta:
        """Setup the factory model."""

        model = Image

    _links = factory.SubFactory(LinksFactory)
    _media = factory.SubFactory(MediaFactory)
    image_md5 = factory.LazyAttribute(lambda _: faker.md5(raw_output=False))
    source = factory.LazyAttribute(lambda _: faker.words(nb=1))


class MetadataFactory(ResourceCommonFactory):
    """Create LTU Cloud metadata objects."""

    class Meta:
        """Setup the factory model."""

        model = Metadata

    _links = factory.SubFactory(LinksFactory)
    key = factory.LazyAttribute(lambda _: faker.words(nb=1))
    ordering = factory.Sequence(lambda n: n)
    value = factory.LazyAttribute(lambda _: faker.words(nb=1))


class VisualFactory(ResourceCommonFactory):
    """Create LTU Cloud visual objects."""

    class Meta:
        """Setup the factory model."""

        model = Visual

        # the following attributes won't be passed to the model class. They're just used as switches
        # or to compute other attributes
        exclude = ("nb_images", "nb_metadatas")

    _links = factory.SubFactory(LinksFactory)
    _media = factory.SubFactory(MediaFactory)
    nb_images = 1  # number of images to associate to this visual
    title = factory.LazyAttribute(lambda _: faker.words(nb=1))
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
