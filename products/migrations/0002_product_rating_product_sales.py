# Generated by Django 5.1.6 on 2025-06-19 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
