# Generated by Django 2.2 on 2019-05-22 10:32

import datetime
from django.conf import settings
from django.db import migrations, models
import lex_pusher.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('solo_mmr', models.CharField(max_length=120)),
                ('party_mmr', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=lex_pusher.models.image_folder)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmr_from', models.IntegerField()),
                ('mmr_to', models.IntegerField()),
                ('steam_login', models.CharField(max_length=120)),
                ('steam_password', models.CharField(max_length=120)),
                ('start_date', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Buster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=120)),
                ('email', models.EmailField(default='0@gmail.com', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BuyAccount',
            fields=[
                ('account_slug', models.SlugField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=120)),
                ('skype', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.IntegerField(null=True)),
                ('mmr', models.FloatField()),
                ('time', models.DateTimeField()),
                ('bust_id', models.ForeignKey(on_delete=True, to='lex_pusher.Bust')),
            ],
        ),
        migrations.AddField(
            model_name='bust',
            name='buster_id',
            field=models.ForeignKey(null=True, on_delete=True, to='lex_pusher.Buster'),
        ),
        migrations.AddField(
            model_name='bust',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
