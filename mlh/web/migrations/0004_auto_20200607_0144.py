# Generated by Django 3.0.6 on 2020-06-06 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0003_auto_20200606_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='img',
            field=models.ImageField(default='web/static/avatars/default.png', upload_to='web/static/avatars/'),
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='victim', to=settings.AUTH_USER_MODEL)),
                ('out_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]