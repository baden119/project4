# Generated by Django 3.1.1 on 2020-09-30 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_post_is_liked_by_current_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_likes',
            field=models.IntegerField(default=0),
        ),
    ]