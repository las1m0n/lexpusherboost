# Generated by Django 2.2 on 2019-05-10 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0013_auto_20190510_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stat',
            name='match_id',
            field=models.IntegerField(null=True),
        ),
    ]
