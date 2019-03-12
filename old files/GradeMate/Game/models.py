from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField('User ID', max_length=10, primary_key=True)
    user_name = models.CharField('User Name', max_length=20)

    def __str_(self):
        return self.user_name

class Group(models.Model):
    group_id = models.CharField('Group ID', max_length=10, primary_key=True)
    group_name = models.CharField('Group Name', max_length=20)

    def __str__(self):
        return self.group_name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credits = models.PositiveIntegerField('Group Credits')

    def __str__(self):
        return self.user

class Exam(models.Model):
    exam_id = models.CharField('Exam ID', max_length=10, primary_key=True)
    group = models.ForeignKey(Group, models.CASCADE)

    def __str__(self):
        return self.exam_id

class Bet(models.Model):
    bet_id = models.CharField('Bet ID', max_length=10, primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    guess_mark = models.PositiveIntegerField('Guessed Mark')
    win = models.NullBooleanField('Winning Bet', default=None, blank=True)

    def __str__(self):
        return self.bet_id

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.PositiveIntegerField('Mark')

    def __str__(self):
        return self.mark
