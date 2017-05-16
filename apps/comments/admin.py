from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'time_created', 'content_type')
    list_filter = ('time_created', 'content_type')
    ordering = ('-time_created',)
    search_fields = ('content', 'author__last_name', 'author__first_name', 'author__email', 'author__username')
