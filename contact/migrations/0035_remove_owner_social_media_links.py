# Generated by Django 5.0.1 on 2024-04-09 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0034_alter_owner_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='social_media_links',
        ),
    ]
