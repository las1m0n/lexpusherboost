# Generated by Django 2.1.5 on 2019-07-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='mmr_current',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stat',
            name='mmr',
            field=models.IntegerField(),
        ),
    ]