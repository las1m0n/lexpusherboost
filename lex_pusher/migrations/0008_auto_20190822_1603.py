# Generated by Django 2.2.4 on 2019-08-22 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0007_auto_20190820_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email_login',
            field=models.CharField(default=0, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='email_password',
            field=models.CharField(default=0, max_length=120),
            preserve_default=False,
        ),
    ]