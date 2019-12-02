from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.models import BaseModel

User = get_user_model()


class FirebaseUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='firebase_user')
    uid = models.CharField(max_length=255)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    photo_url = models.URLField(max_length=255, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
