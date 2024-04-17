# Generated by Django 4.2 on 2024-04-17 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0007_remove_category_parent_category_category_subcategory"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(help_text="Почта", max_length=254)),
                (
                    "name",
                    models.CharField(help_text="Имя пользователя", max_length=255),
                ),
                ("comment", models.TextField(help_text="Комментарий")),
                (
                    "phone",
                    models.CharField(
                        help_text="Номер телефона",
                        max_length=12,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введите номер телефона в формате + 7 123 456 7890",
                                regex="^((\\+7|7|8)+([0-9]){10})$",
                            )
                        ],
                    ),
                ),
            ],
        ),
    ]
