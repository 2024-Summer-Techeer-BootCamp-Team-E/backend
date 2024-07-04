# Generated by Django 4.2.8 on 2024-07-04 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
