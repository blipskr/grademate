# Generated by Django 2.1.5 on 2019-03-06 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('bet_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Bet ID')),
                ('guess_mark', models.PositiveIntegerField(verbose_name='Guessed Mark')),
                ('win', models.BooleanField(blank=True, default=None, null=True, verbose_name='Winning Bet')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Exam ID')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Group ID')),
                ('group_name', models.CharField(max_length=20, verbose_name='Group Name')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credits', models.PositiveIntegerField(verbose_name='Group Credits')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.PositiveIntegerField(verbose_name='Mark')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='User ID')),
                ('user_name', models.CharField(max_length=20, verbose_name='User Name')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.User'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.User'),
        ),
        migrations.AddField(
            model_name='exam',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Group'),
        ),
        migrations.AddField(
            model_name='bet',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Exam'),
        ),
        migrations.AddField(
            model_name='bet',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='Game.User'),
        ),
        migrations.AddField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='Game.User'),
        ),
    ]
