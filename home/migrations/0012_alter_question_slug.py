# Generated by Django 5.0.6 on 2024-07-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_answer_options_alter_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(),
        ),
    ]