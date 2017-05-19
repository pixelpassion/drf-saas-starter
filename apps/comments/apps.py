from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'apps.comments'
    verbose_name = "Comments"

    def ready(self):
        """If django-activity-stream is installed, register the Comment model for usage."""
        try:
            from actstream import registry
            registry.register(self.get_model('Comment'))
        except ImportError:
            pass
