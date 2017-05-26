import factory

from django.contrib.contenttypes.models import ContentType

from apps.users.tests.factories import UserFactory


class CommentFactory(factory.django.DjangoModelFactory):
    """An abstract CommentFactory to inherit from, because of the GenericForeignKey that is used."""
    author = factory.SubFactory(UserFactory)
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    content = factory.Sequence(lambda n: f"Comment #{n + 1}")

    class Meta:
        exclude = ['content_object']
        abstract = True


class CommentUserFactory(CommentFactory):
    """A Factory for comments on users."""
    content_object = factory.SubFactory(UserFactory)

    class Meta:
        model = 'comments.Comment'
