# Generated by Django 5.0.1 on 2024-01-24 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_alter_owner_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='user',
        ),
    ]