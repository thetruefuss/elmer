from django.contrib import admin

from .models import Profile, Notification


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin settings for profiles.
    """
    list_display = ('user', 'dob', 'member_since')
    date_hierarchy = 'member_since'
admin.site.register(Profile, ProfileAdmin)  # noqa: E305


class NotifyAdmin(admin.ModelAdmin):
    """
    Admin settings for notifications.
    """
    list_display = ('notif_type', 'Actor', 'Object', 'Target', 'is_read', 'created')
    list_filter = ('is_read',)
    date_hierarchy = 'created'
admin.site.register(Notification, NotifyAdmin)  # noqa: E305
