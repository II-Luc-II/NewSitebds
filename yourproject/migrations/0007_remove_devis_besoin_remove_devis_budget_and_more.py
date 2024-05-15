# Generated by Django 5.0.4 on 2024-05-13 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourproject', '0006_devis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devis',
            name='besoin',
        ),
        migrations.RemoveField(
            model_name='devis',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='devis',
            name='date',
        ),
        migrations.RemoveField(
            model_name='devis',
            name='description',
        ),
        migrations.RemoveField(
            model_name='devis',
            name='posted_date',
        ),
        migrations.AddField(
            model_name='question',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]