# Generated by Django 2.1.5 on 2019-05-03 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0004_boost'),
    ]

    operations = [
        migrations.AddField(
            model_name='boost',
            name='email',
            field=models.EmailField(default='0@gmail.com', max_length=254),
        ),
    ]