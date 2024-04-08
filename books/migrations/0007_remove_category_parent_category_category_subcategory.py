# Generated by Django 4.2 on 2024-04-07 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0006_remove_category_subcategory_category_parent_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="parent_category",
        ),
        migrations.AddField(
            model_name="category",
            name="subcategory",
            field=models.ForeignKey(
                blank=True,
                help_text="Дочерняя категория книг",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="books.category",
            ),
        ),
    ]