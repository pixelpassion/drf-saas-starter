import builtins

from django.test import TestCase

from apps.comments.models import Comment
from apps.users.tests.factories import UserFactory


class TestCreateComment(TestCase):

    def test_create_comment(self):
        author = UserFactory()
        commented_user = UserFactory()
        Comment.objects.create(author=author, content_object=commented_user, content="A comment.")


class TestCreateCommentActstreamImportError(TestCase):
    """Creating comments should work when actstream is not importable."""

    def setUp(self):
        """Use import_hook to make actstream not available."""

        def import_hook(name, *args, **kwargs):
            if name == 'actstream':
                raise ImportError('test case module import failure')
            else:
                return self.original_imports(name, *args, **kwargs)

        self.original_imports = builtins.__import__
        builtins.__import__ = import_hook

    def test_create_comment_without_actstream(self):
        author = UserFactory()
        commented_user = UserFactory()
        Comment.objects.create(author=author, content_object=commented_user, content="A comment.")

    def tearDown(self):
        """Restore normal import behaviour."""
        builtins.__import__ = self.original_imports
