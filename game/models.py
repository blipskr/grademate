from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Group(models.Model):
    group_id = models.AutoField('Group ID', primary_key=True)
    group_name = models.CharField('Group Name', max_length=20)

    def __unicode__(self):
        return self.group_name


class GroupMember(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    credits = models.PositiveIntegerField('Group Credits')

    def __unicode__(self):
        return self.group


class Exam(models.Model):
    exam_id = models.AutoField('Exam ID', primary_key=True)
    group = models.ForeignKey(Group)
    exam_name = models.CharField('Exam Name', max_length=40)

    def __unicode__(self):
        return self.exam_name


class Bet(models.Model):
    bet_id = models.AutoField('Bet ID', primary_key=True)
    exam = models.ForeignKey(Exam)
    user = models.ForeignKey(User, related_name='creator',)
    target = models.ForeignKey(User, related_name='target')
    guess_mark = models.PositiveIntegerField('Guessed Mark')
    guess_credits = models.PositiveIntegerField('Guessed Credits')
    win = models.NullBooleanField('Winning Bet', default=None, blank=True)

    def __unicode__(self):
        return self.bet_id


class Result(models.Model):
    exam = models.ForeignKey(Exam)
    user = models.ForeignKey(User)
    mark = models.PositiveIntegerField('Mark')

    def __unicode__(self):
        return self.mark
