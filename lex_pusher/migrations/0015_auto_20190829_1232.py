# Generated by Django 2.2.4 on 2019-08-29 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0014_auto_20190828_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bust',
            name='buster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lex_pusher.Buster'),
        ),
    ]
