# Generated by Django 4.1 on 2023-03-02 19:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game_app", "0002_battle_ship_death_soldiers_ship_destroyed_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ship",
            name="eligible_soldiers",
            field=models.IntegerField(),
        ),
    ]