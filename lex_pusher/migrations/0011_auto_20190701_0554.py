# Generated by Django 2.2 on 2019-07-01 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0010_auto_20190627_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buster',
            name='avatar',
            field=models.ImageField(blank=True, default='ссс/ccc.png', null=True, upload_to=''),
        ),
    ]
