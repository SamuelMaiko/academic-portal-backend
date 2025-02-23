# Generated by Django 5.0.2 on 2025-02-23 12:41

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_work', '0010_alter_type_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workimage',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='academic-portal/work-images/'),
        ),
    ]
