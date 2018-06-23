from django.contrib import admin

from .models import Blog_Feedback, Comment, Image, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Blog_Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
