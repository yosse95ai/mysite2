# Generated by Django 3.1.6 on 2021-02-17 03:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ranges', '0006_auto_20210217_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='range',
            name='arranger',
        ),
        migrations.AddField(
            model_name='song',
            name='arranger',
            field=models.ManyToManyField(blank=True, null=True, related_name='arranger_name', to='ranges.Artist'),
        ),
        migrations.AlterField(
            model_name='range',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 17, 3, 47, 14, 509063, tzinfo=utc)),
        ),
    ]
