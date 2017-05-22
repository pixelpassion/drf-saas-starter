import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Comment(models.Model):

    id = models.UUIDField(_('ID'), primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    # This enables the GenericForeignKey to comment any object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=36)
    content_object = GenericForeignKey('content_type', 'object_id')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        help_text=_("Who wrote the comment?"),
        related_name='comments',
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        _("content"),
        help_text=_("The text of the comment"),
    )

    time_created = models.DateTimeField(
        _("Creation time"),
        help_text=_("When was the comment created?"),
        default=timezone.now,
        editable=False,
    )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return f"{self.time_created.isoformat(timespec='seconds')} " \
               f"{self.author}: " \
               f"{self.content[:50]}{'' if len(self.content) < 50 else '...'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            from actstream import action
            action.send(self.author, verb='made comment', action_object=self, target=self.content_object)
        except ImportError:
            pass
