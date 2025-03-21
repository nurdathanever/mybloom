# Generated by Django 5.1.6 on 2025-03-19 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_custom_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ai_bouquet_image',
            field=models.ImageField(blank=True, null=True, upload_to='ai_bouquets/'),
        ),
        migrations.AddField(
            model_name='order',
            name='greeting_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
    ]
