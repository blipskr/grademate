# Generated by Django 2.1.5 on 2019-03-11 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='win',
            field=models.NullBooleanField(default=None, verbose_name='Winning Bet'),
        ),
    ]
