# Generated by Django 5.1.2 on 2024-10-22 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.category'),
        ),
    ]