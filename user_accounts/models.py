from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from frontboard.models import Subject


class Profile(models.Model):
    """
    Model that represents a profile.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    dp = models.ImageField(upload_to='dps/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    followers = models.ManyToManyField(User, related_name='following', blank=True)
    contact_list = models.ManyToManyField(User, related_name='contacters', blank=True)
    pending_list = models.ManyToManyField(User, related_name='my_pending_requests', blank=True)

    member_since = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-member_since', )

    def __str__(self):
        """
        Unicode representation for a profile model.

        :return: string
        """
        return self.user.username

    def screen_name(self):
        """
        Returns screen name.

        :return: string
        """
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:  # noqa: E722
            return self.user.username

    def get_picture(self):
        """
        Returns profile picture url (if any).

        :return: string
        """
        default_picture = settings.STATIC_URL + 'img/ditto.jpg'
        if self.dp:
            return self.dp.url
        else:
            return default_picture


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Signals the Profile about User creation.

    :return:
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Notification(models.Model):
    """
    Model that represents a notification.
    """

    NOTIF_CHOICES = (
        ('subject_mentioned', 'Mentioned in Subject'),
        ('comment_mentioned', 'Mentioned in Comment'),
        ('comment', 'Comment on Subject'),
        ('follow', 'Followed by someone'),
        ('sent_msg_request', 'Sent a Message Request'),
        ('confirmed_msg_request', 'Sent a Message Request'),
    )

    Actor = models.ForeignKey(User, related_name='c_acts')
    Object = models.ForeignKey(Subject, related_name='act_notif', null=True, blank=True)
    Target = models.ForeignKey(User, related_name='c_notif')
    notif_type = models.CharField(max_length=500,
                                  choices=NOTIF_CHOICES,
                                  default='Comment on Subject')

    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-created',)

    def __str__(self):
        """
        Unicode representation for a notification based on notification type.

        :return: string
        """
        if self.notif_type == 'comment':
            return '{} commented on your subject \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )
        elif self.notif_type == 'subject_mentioned':
            return '{} mentioned you in his subject \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )
        elif self.notif_type == 'follow':
            return '{} followed you.'.format(
                self.Actor.profile.screen_name()
            )
        elif self.notif_type == 'sent_msg_request':
            return '{} sent you a message request.'.format(
                self.Actor.profile.screen_name()
            )
        elif self.notif_type == 'confirmed_msg_request':
            return '{} accepted your message request.'.format(
                self.Actor.profile.screen_name()
            )
        else:
            return '{} mentioned you in his comment on subject \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )

    @staticmethod
    def get_user_notification(user):
        """
        Returns user notifications.

        :param user: Object
        :return: list
        """
        if user:
            notifications = Notification.objects.filter(Target=user).exclude(Actor=user)
            return notifications
        return []
