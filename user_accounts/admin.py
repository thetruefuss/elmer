from django.contrib import admin

from .models import Profile, subject_notify


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'member_since')
    date_hierarchy = 'member_since'
admin.site.register(Profile, ProfileAdmin)  # noqa: E305


@admin.register(subject_notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ('notif_type', 'Actor', 'Object', 'Target', 'is_read', 'created')
