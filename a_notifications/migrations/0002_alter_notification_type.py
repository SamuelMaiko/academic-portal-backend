# Generated by Django 5.0.2 on 2024-07-17 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('Nearing Deadline', 'Nearing Deadline'), ('New Revision', 'New Revision'), ('Update Profile', 'Update Profile'), ('System Notification', 'System Notification'), ('Revoked Work', 'Revoked Work'), ('Uptaken Work', 'Uptaken Work'), ('Assigned Work', 'Assigned Work')], max_length=50),
        ),
    ]
