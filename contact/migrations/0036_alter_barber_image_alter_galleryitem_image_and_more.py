# Generated by Django 5.0.1 on 2024-04-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0035_remove_owner_social_media_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barber',
            name='image',
            field=models.ImageField(upload_to='static/barber_images/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='galleryitem',
            name='image',
            field=models.ImageField(upload_to='static/gallery_images/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='static/owner_logos/', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/review_images/', verbose_name='Foto'),
        ),
    ]
