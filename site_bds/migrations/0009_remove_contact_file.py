# Generated by Django 5.0.4 on 2024-05-07 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_bds', '0008_contact_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='file',
        ),
    ]
