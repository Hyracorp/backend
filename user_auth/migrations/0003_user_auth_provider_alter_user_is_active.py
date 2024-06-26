# Generated by Django 5.0.4 on 2024-05-05 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_auth", "0002_user_is_verified"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="auth_provider",
            field=models.CharField(
                choices=[
                    ("email", "email"),
                    ("google", "google"),
                    ("facebook", "facebook"),
                ],
                default="email",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
