# Generated by Django 4.1.4 on 2023-02-21 01:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_control', '0022_alter_verifycode_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='expiration_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 21, 1, 29, 32, 960154, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]