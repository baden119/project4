# Generated by Django 3.1.1 on 2020-09-16 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='network.user'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'followed_by')},
        ),
        migrations.RemoveField(
            model_name='follow',
            name='follower_of',
        ),
    ]