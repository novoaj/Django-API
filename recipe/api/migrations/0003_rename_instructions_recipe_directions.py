# Generated by Django 5.0.6 on 2024-07-24 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='instructions',
            new_name='directions',
        ),
    ]
