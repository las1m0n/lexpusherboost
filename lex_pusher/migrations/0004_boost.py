# Generated by Django 2.1.5 on 2019-05-02 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0003_auto_20190502_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmr_from', models.IntegerField()),
                ('mmr_to', models.IntegerField()),
                ('login', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
                ('more_info', models.BooleanField(blank=True, null=True)),
                ('vk', models.CharField(max_length=120)),
                ('skype', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
            ],
        ),
    ]
