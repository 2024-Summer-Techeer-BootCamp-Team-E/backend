# Generated by Django 4.2.8 on 2024-07-20 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]