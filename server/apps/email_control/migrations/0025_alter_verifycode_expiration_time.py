# Generated by Django 4.1.4 on 2023-02-21 01:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_control', '0024_alter_verifycode_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='expiration_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 21, 1, 44, 49, 278615, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
