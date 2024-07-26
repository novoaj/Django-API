# Generated by Django 5.0.6 on 2024-07-23 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
                ('servings', models.CharField(max_length=255, null=True)),
                ('prep_time', models.CharField(max_length=255, null=True)),
                ('cook_time', models.CharField(max_length=255, null=True)),
                ('total_time', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]