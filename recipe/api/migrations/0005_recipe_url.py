# Generated by Django 5.0.6 on 2024-07-24 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='url',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
