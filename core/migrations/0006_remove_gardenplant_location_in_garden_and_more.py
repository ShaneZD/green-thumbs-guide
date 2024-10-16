# Generated by Django 5.1 on 2024-10-10 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_plant_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gardenplant',
            name='location_in_garden',
        ),
        migrations.AlterField(
            model_name='gardenplant',
            name='garden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.garden'),
        ),
        migrations.AlterField(
            model_name='gardenplant',
            name='last_fertilized',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gardenplant',
            name='last_pruned',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gardenplant',
            name='last_watered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gardenplant',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
