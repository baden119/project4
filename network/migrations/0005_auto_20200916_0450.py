# Generated by Django 3.1.1 on 2020-09-16 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200916_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='network.user'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'following')},
        ),
        migrations.RemoveField(
            model_name='follow',
            name='followed_by',
        ),
    ]
