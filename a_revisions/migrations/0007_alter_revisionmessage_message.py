# Generated by Django 5.0.2 on 2024-07-28 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_revisions', '0006_alter_revision_opened_by_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisionmessage',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
