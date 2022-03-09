# Generated by Django 4.0.3 on 2022-03-09 19:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_route'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='route',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='route',
            name='city',
        ),
        migrations.RemoveField(
            model_name='route',
            name='route_id',
        ),
        migrations.RemoveField(
            model_name='route',
            name='route_order',
        ),
        migrations.CreateModel(
            name='RouteCities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_order', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Order')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.city', verbose_name='City')),
                ('route_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.route', verbose_name='Route ID')),
            ],
            options={
                'verbose_name': 'Route Cities',
                'verbose_name_plural': 'Route Cities',
                'unique_together': {('route_id', 'city')},
            },
        ),
    ]
