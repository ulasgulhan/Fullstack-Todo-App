# Generated by Django 5.0.4 on 2024-05-03 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0003_alter_task_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="user_id",
            new_name="user",
        ),
    ]
