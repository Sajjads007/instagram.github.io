# Generated by Django 5.1.6 on 2025-02-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_remove_useraccount_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='user_followers', to='posts.useraccount'),
        ),
    ]
