# Generated by Django 5.1.2 on 2024-11-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0004_remove_employee_level_employee_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='status',
            field=models.CharField(choices=[('running', 'Running'), ('closed', 'Closed')], default='running', max_length=10),
        ),
    ]