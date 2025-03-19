# Generated by Django 5.1.6 on 2025-03-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='flower_ingredients',
            field=models.ManyToManyField(blank=True, limit_choices_to={'category': 'flower'}, to='products.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='seasonality',
            field=models.CharField(blank=True, choices=[('spring', 'Spring'), ('summer', 'Summer'), ('autumn', 'Autumn'), ('winter', 'Winter')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='style',
            field=models.CharField(blank=True, choices=[('classic', 'Classic'), ('minimalistic', 'Minimalistic'), ('exotic', 'Exotic'), ('lush', 'Lush'), ('mono', 'Mono')], max_length=20, null=True),
        ),
    ]
