# Generated by Django 4.2.2 on 2024-03-11 04:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dat_app", "0003_rename_user_dat_test_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dat_test",
            name="username",
        ),
    ]
