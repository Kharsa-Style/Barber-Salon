# Generated by Django 5.0.1 on 2024-03-14 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0028_alter_product_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Slug'),
        ),
    ]
