# Generated by Django 4.2.3 on 2023-07-22 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0003_remove_workspacesusers_user_workspacesusers_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspaces',
            name='admin',
        ),
    ]
