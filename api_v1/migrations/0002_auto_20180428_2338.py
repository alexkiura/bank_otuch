# Generated by Django 2.0.4 on 2018-04-28 23:38

import api_v1.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bankinguser',
            managers=[
                ('objects', api_v1.models.UserManager()),
            ],
        ),
    ]
