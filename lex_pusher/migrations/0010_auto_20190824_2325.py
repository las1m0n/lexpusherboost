# Generated by Django 2.2.4 on 2019-08-24 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0009_auto_20190822_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buster',
            name='avatar',
            field=models.ImageField(blank=True, default='dota-2.png', null=True, upload_to=''),
        ),
    ]
