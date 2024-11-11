# Generated by Django 5.1.2 on 2024-11-10 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0010_rename_evalaution_approval_evaluation'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=20)),
                ('final_score', models.IntegerField()),
                ('score', models.CharField(max_length=2)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.evaluation')),
            ],
        ),
    ]
