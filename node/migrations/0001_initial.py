# Generated by Django 3.1.4 on 2020-12-27 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=200, unique=True, verbose_name='Device Name')),
                ('power_state', models.BooleanField(default=False, verbose_name='Power State')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(verbose_name='Temperature')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='node.node')),
            ],
        ),
    ]
