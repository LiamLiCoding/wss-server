# Generated by Django 4.1.7 on 2023-03-04 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(editable=False, max_length=150)),
                ('name', models.CharField(default=None, max_length=200)),
                ('status', models.CharField(choices=[('expired', 'Expired'), ('disable', 'Disable'), ('enable', 'Enable')], default='enable', max_length=50)),
                ('suc_conv_num', models.PositiveIntegerField(default=0)),
                ('failed_conv_num', models.PositiveIntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'API key',
                'verbose_name_plural': 'API keys',
                'ordering': ('-created_time',),
            },
        ),
    ]