# Generated by Django 5.1.6 on 2025-02-20 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_useraccount_remove_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='follow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='followers',
            field=models.ManyToManyField(related_name='user_followers', to='posts.useraccount'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='following',
            field=models.ManyToManyField(related_name='user_following', to='posts.useraccount'),
        ),
    ]
