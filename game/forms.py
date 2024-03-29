from django import forms
from models import Bet, Result, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from models import Exam, Group
import dbqueries as query

from django.core.exceptions import ValidationError


class JoinGroupForm(forms.Form):

    group_name = forms.CharField()
    group_id = forms.CharField()

    class Meta:

        fields = ('group_name', 'group_id')

    def __init__(self, *args, **kwargs):
        super(JoinGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_name'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'groupname'})
        self.fields['group_id'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'groupid'})


class EnterBetForm(forms.ModelForm):
    exam = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))
    target = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))

    class Meta:
        model = Bet
        fields = ('exam', 'target', 'guess_mark', 'guess_credits', 'user')

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        self.user = kwargs.pop('user')
        super(EnterBetForm, self).__init__(*args, **kwargs)
        self.fields['guess_mark'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'guess_mark'})
        self.fields['guess_credits'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'guess_credits'})
        groupusers = query.userIDsinGroup(self.group)
        groupexams = query.examIDsinGroup(self.group)
        user = self.user.id
        self.fields['target'].queryset = User.objects.filter(
            pk__in=groupusers).exclude(pk=user).order_by('username')
        self.fields['exam'].queryset = Exam.objects.filter(
            pk__in=groupexams).order_by('exam_id')
        self.fields['exam'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'chooseexam'})
        self.fields['exam'].widget.attrs['readonly'] = True
        self.fields['target'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'choosetarget'})
        self.fields['target'].widget.attrs['readonly'] = True
        self.fields['user'] = self.user
        self.fields['user'].widget = forms.HiddenInput()


class UpdateBetForm(forms.Form):
    bet = forms.ModelChoiceField(queryset=Bet.objects.filter(pk=1))
    mark = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.myBets = kwargs.pop('bets')
        super(UpdateBetForm, self).__init__(*args, **kwargs)
        self.fields['bet'].queryset = self.myBets
        self.fields['mark'].widget = forms.TextInput()
        self.fields['bet'].required = False
        self.fields['mark'].required = False
        self.fields['mark'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'newmark', 'pattern': '-?[0-9]*(\.[0-9]+)?'})
        self.fields['bet'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'updatebet'})
        self.fields['bet'].widget.attrs['readonly'] = True


class EnterMarksForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))
    mark = forms.CharField()

    class Meta:
        fields = ('exam', 'mark', 'user')

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super(EnterMarksForm, self).__init__(*args, **kwargs)
        exams = query.retrieveGroupExams(self.group)
        self.fields['exam'].queryset = exams
        self.fields['exam'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'chooseexam'})
        self.fields['exam'].widget.attrs['readonly'] = True
        self.fields['mark'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'mark'})


class CreateGroupForm(forms.Form):
    group_name = forms.CharField(label='Group name', max_length=20)

    class Meta:
        model = Group
        fields = ('group_name')

    def __init__(self, *args, **kwargs):
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_name'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'creategroup'})


class AddExamForm(forms.Form):
    exam_name = forms.CharField(label='Exam name', max_length=20)

    class Meta:
        model = Exam
        fields = ('exam')

    def __init__(self, *args, **kwargs):
        super(AddExamForm, self).__init__(*args, **kwargs)
        self.fields['exam_name'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'addexam'})

class DeleteExamForm(forms.Form):
    exam_name = forms.CharField(label='Exam name', max_length=20)

    def __init__(self, *args, **kwargs):
        super(DeleteExamForm, self).__init__(*args, **kwargs)
        self.fields['exam_name'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'removeexam'})

class AddUserToGroupForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=20)

    def __init__(self, *args, **kwargs):
        super(AddUserToGroupForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'adduser'})


class DeleteUserForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=20)

    def __init__(self, *args, **kwargs):
        super(DeleteUserForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'removeuser'})
