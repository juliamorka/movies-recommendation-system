# Generated by Django 4.2.6 on 2023-10-23 20:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="imdb_id",
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]