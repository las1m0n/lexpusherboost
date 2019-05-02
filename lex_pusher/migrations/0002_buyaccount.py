# Generated by Django 2.1.5 on 2019-05-02 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lex_pusher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=120)),
                ('skype', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
                ('account', models.ForeignKey(on_delete=True, to='lex_pusher.Account')),
            ],
        ),
    ]