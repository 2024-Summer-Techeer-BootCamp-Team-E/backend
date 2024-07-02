# Generated by Django 4.2.8 on 2024-07-02 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('category_id', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency_id', models.IntegerField()),
                ('link', models.URLField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]
