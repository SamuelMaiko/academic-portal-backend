# Generated by Django 5.0.2 on 2024-07-17 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_revisions', '0004_alter_revisionmessage_file_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='revision',
            options={'ordering': ['-created_at']},
        ),
    ]
