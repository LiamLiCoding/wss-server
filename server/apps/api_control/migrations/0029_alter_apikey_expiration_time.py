# Generated by Django 4.1.4 on 2023-02-27 02:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_control', '0028_alter_apikey_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='expiration_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 26, 2, 23, 29, 885000, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
