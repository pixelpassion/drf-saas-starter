import builtins

from django.test import TestCase

from apps.comments.apps import CommentsConfig


class TestActstreamImportError(TestCase):

    def setUp(self):
        """Use import_hook to make actstream not available."""

        def import_hook(name, *args, **kwargs):
            if name == 'actstream':
                raise ImportError('test case module import failure')
            else:
                return self.original_imports(name, *args, **kwargs)

        self.original_imports = builtins.__import__
        builtins.__import__ = import_hook

    def test_raise_import_error(self):
        """Call ready() on CommentsConfig.

        As Python doesn't support unloading of modules, calling the method ready(),
        while importing actstream is disabled, must suffice.
        """
        CommentsConfig.ready(self)

    def tearDown(self):
        """Restore normal import behaviour."""
        builtins.__import__ = self.original_imports
