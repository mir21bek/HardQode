# Generated by Django 5.0.2 on 2024-03-02 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_customuser_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="otp",
            field=models.PositiveIntegerField(max_length=4, null=True),
        ),
    ]
