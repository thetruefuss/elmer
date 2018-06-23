from django.contrib import admin

from .models import Board, Comment, FeaturedPost, Report, Subject


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_admins', 'created', 'updated')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'commenter', 'created', 'active')
    list_filter = ('commenter', 'active', 'created', 'updated')
    search_fields = ('user', 'body')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'created', 'active')
    list_filter = ('title', 'active')
    date_hierarchy = 'created'


admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(FeaturedPost)
admin.site.register(Report)
