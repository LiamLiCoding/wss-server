# Generated by Django 4.1.7 on 2023-04-13 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_verifycode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='detection_Email_notification',
            field=models.BooleanField(default=False),
        ),
    ]