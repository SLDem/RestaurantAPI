# Generated by Django 4.2.5 on 2023-09-12 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurants", "0004_remove_menuitem_day_menu_day"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="day",
            field=models.DateField(default=datetime.date(2023, 9, 12), unique=True),
        ),
    ]