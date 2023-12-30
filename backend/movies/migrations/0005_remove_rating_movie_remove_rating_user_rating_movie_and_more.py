# Generated by Django 4.2.6 on 2023-12-17 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("movies", "0004_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rating",
            name="movie",
        ),
        migrations.RemoveField(
            model_name="rating",
            name="user",
        ),
        migrations.AddField(
            model_name="rating",
            name="movie",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="movies.movie",
            ),
        ),
        migrations.AddField(
            model_name="rating",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]