# Generated by Django 4.2.8 on 2024-07-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='category_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='search',
            name='keyword',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
