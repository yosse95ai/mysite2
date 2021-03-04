# Generated by Django 3.1.6 on 2021-03-04 13:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ranges', '0013_auto_20210304_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='range',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 4, 13, 7, 48, 860817, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='range',
            unique_together={('song', 'artist', 'origin')},
        ),
    ]
