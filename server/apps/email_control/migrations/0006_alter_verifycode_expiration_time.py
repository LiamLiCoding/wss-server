# Generated by Django 4.1.4 on 2023-02-04 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_control', '0005_alter_verifycode_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='expiration_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 4, 6, 35, 53, 961929, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]