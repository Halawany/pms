# Generated by Django 5.1.2 on 2024-11-10 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0008_alter_userscore_score'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=20)),
                ('hr_approval', models.BooleanField(default=False)),
                ('evalaution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.evaluation')),
                ('hr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]