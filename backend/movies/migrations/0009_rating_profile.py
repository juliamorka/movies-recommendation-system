# Generated by Django 4.2.6 on 2024-01-12 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0008_alter_profile_cluster"),
    ]

    operations = [
        migrations.AddField(
            model_name="rating",
            name="profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="movies.profile",
            ),
        ),
    ]