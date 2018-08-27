from django.contrib import admin

from .models import Board, Comment, Report, Subject


class BoardAdmin(admin.ModelAdmin):
    """
    Admin settings for boards.
    """
    list_display = ('title', 'created', 'updated')
    date_hierarchy = 'created'
admin.site.register(Board, BoardAdmin)  # noqa: E305


class CommentAdmin(admin.ModelAdmin):
    """
    Admin settings for comments.
    """
    list_display = ('body', 'commenter', 'created', 'active')
    list_filter = ('commenter', 'active')
    date_hierarchy = 'created'
admin.site.register(Comment, CommentAdmin)  # noqa: E305


class SubjectAdmin(admin.ModelAdmin):
    """
    Admin settings for subjects.
    """
    list_display = ('title', 'board', 'created', 'active')
    list_filter = ('title', 'active')
    date_hierarchy = 'created'
admin.site.register(Subject, SubjectAdmin)  # noqa: E305


class ReportAdmin(admin.ModelAdmin):
    """
    Admin settings for reports.
    """
    list_display = ('reporter', 'created', 'active')
    list_filter = ('active',)
    date_hierarchy = 'created'
admin.site.register(Report, ReportAdmin)  # noqa: E305
