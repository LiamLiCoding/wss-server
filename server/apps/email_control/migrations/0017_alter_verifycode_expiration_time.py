# Generated by Django 4.1.4 on 2023-02-13 16:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_control', '0016_alter_verifycode_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='expiration_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 13, 16, 49, 53, 877781, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]