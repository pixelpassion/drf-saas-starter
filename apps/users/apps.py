from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = "Users"

    def ready(self):
        """If django-activity-stream is installed, register the User model for usage."""
        try:
            from actstream import registry
            registry.register(self.get_model('User'))
        except ImportError:
            pass
