from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    img = models.ImageField(upload_to='mlh/web/static/avatars/', default='mlh/web/static/avatars/default.png')


class ChooseGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    goal = models.CharField(max_length=50)
    level = models.IntegerField()

# Create your models here.
