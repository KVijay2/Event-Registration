# Generated by Django 4.0 on 2022-10-08 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='event_participant',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
