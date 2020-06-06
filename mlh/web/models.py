from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    img = models.ImageField(upload_to='web/static/avatars/', default='web/static/avatars/default.png')


class ChooseGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    goal = models.CharField(max_length=50)
    level = models.IntegerField()


class Friends(models.Model):
    out_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator")
    in_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="victim")

# Create your models here.
