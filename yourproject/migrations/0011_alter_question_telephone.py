# Generated by Django 5.0.4 on 2024-05-14 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourproject', '0010_remove_choice_question_remove_description_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='telephone',
            field=models.CharField(max_length=255),
        ),
    ]
