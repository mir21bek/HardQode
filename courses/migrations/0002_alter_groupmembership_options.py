# Generated by Django 5.0.2 on 2024-03-02 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="groupmembership",
            options={
                "verbose_name": "Участники группы",
                "verbose_name_plural": "Участники группы",
            },
        ),
    ]