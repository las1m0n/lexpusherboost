# Generated by Django 2.2.4 on 2019-08-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0004_calibration'),
    ]

    operations = [
        migrations.AddField(
            model_name='bust',
            name='mmr_type',
            field=models.CharField(default='none', max_length=120),
        ),
    ]
