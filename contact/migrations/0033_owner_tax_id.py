# Generated by Django 5.0.1 on 2024-04-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0032_alter_message_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='tax_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
