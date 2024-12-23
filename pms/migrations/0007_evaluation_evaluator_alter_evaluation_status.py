# Generated by Django 5.1.2 on 2024-11-10 07:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0006_template_level'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='evaluator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='status',
            field=models.CharField(choices=[('running', 'Running'), ('Completed', 'Completed'), ('closed', 'Closed')], default='running', max_length=10),
        ),
    ]
