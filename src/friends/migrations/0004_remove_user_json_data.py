# Generated by Django 5.0.6 on 2024-11-05 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0003_remove_user_city_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='json_data',
        ),
    ]
