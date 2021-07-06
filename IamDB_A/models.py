from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class movie(models.Model):
    name = models.CharField(max_length=50, default=None)
    _99popularity = models.IntegerField(default=None)
    director = models.CharField(max_length=30,default=None)
    genre = models.JSONField(default=None)
    score = models.FloatField(default=None)

    def __str__(self):
        return self.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


