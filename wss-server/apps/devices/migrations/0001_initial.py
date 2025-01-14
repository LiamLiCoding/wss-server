# Generated by Django 4.1.7 on 2023-03-29 23:19

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
            name='Devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('node_type', models.CharField(choices=[('IntruderDetect', 'IntruderDetect'), ('Gateway', 'Gateway')], default='motion IntruderDetect', max_length=200)),
                ('device_type', models.CharField(choices=[('RaspberryPi', 'Raspberry Pi')], default='RaspberryPi', max_length=200)),
                ('api_key', models.CharField(editable=False, max_length=150)),
                ('is_activated', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_enable', models.BooleanField(default=True)),
                ('protocol', models.CharField(choices=[('Websocket', 'Websocket')], default='Websocket', max_length=50)),
                ('conversation_num', models.PositiveIntegerField(default=0)),
                ('enable_profiler', models.BooleanField(default=True)),
                ('enable_intruder_detection', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_online', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'devices',
                'verbose_name_plural': 'devices',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_rate', models.DecimalField(decimal_places=1, max_digits=5)),
                ('mem_rate', models.DecimalField(decimal_places=1, max_digits=5)),
                ('disk_write_io', models.BigIntegerField(default=0)),
                ('disk_read_io', models.BigIntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.devices')),
            ],
            options={
                'verbose_name': 'performance',
                'verbose_name_plural': 'performance',
                'ordering': ('-created_time',),
            },
        ),
    ]
