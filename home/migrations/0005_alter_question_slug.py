# Generated by Django 5.0.6 on 2024-07-08 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]