# Generated by Django 2.0.4 on 2018-04-30 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0006_auto_20180430_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
