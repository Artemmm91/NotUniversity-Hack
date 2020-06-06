from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    img = models.ImageField(upload_to='mlh/web/static/avatars/', default='mlh/web/static/avatars/default.png')

# Create your models here.
