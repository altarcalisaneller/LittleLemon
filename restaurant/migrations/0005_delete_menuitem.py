# Generated by Django 4.1 on 2023-07-15 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0004_menuitem"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MenuItem",
        ),
    ]