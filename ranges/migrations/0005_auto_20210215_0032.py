# Generated by Django 3.1.6 on 2021-02-14 15:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ranges', '0004_auto_20210215_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='range',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 14, 15, 32, 57, 614490, tzinfo=utc)),
        ),
    ]
