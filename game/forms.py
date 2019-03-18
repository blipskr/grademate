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
        self.fields['group_name'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id': 'groupname'})
        self.fields['group_id'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id': 'groupid'})


class EnterBetForm(forms.ModelForm):
    exam = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))
    target = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))

    class Meta:
        model = Bet
        fields = ('exam', 'target', 'guess_mark', 'user')

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        self.user = kwargs.pop('user')
        super(EnterBetForm, self).__init__(*args, **kwargs)
        self.fields['guess_mark'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'guess_mark'})
        groupusers = query.userIDsinGroup(self.group)
        groupexams = query.examIDsinGroup(self.group)
        self.fields['target'].queryset = User.objects.filter(pk__in=groupusers)
        self.fields['exam'].queryset = Exam.objects.filter(pk__in=groupexams)
        self.fields['exam'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'chooseexam'})
        self.fields['exam'].widget.attrs['readonly'] = True
        self.fields['target'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'choosetarget'})
        self.fields['target'].widget.attrs['readonly'] = True
        self.fields['user'] = self.user
        self.fields['user'].widget = forms.HiddenInput()

    def clean(self, value):
        cleaned_data = self.cleaned_data
        print 'ok'
        return cleaned_data


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


class EnterMarksForm(forms.ModelForm):
    error_css_class = 'error'
    exam = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))
    mark = forms.IntegerField(label='Mark Estimate',
                              max_value=100, min_value=0)

    class Meta:
        model = Result
        fields = ('exam', 'mark')

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super(EnterMarksForm, self).__init__(*args, **kwargs)

        groupexams = query.examIDsinGroup(self.group)
        self.fields['exam'].queryset = Exam.objects.filter(pk__in=groupexams)
        self.fields['mark'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'markInput'})

        for fieldname in ['exam', 'mark', ]:
            self.fields[fieldname].help_text = None

    def clean(self):
        mark = self.cleaned_data.get('mark')
        if not (mark <= 100 and mark >= 0):
            raise ValidationError("Invalid mark")
        return mark


class ViewMarksForm(forms.ModelForm):
    exam = forms.CharField(label='Exam', max_length=100)
    mark = forms.IntegerField(label='Mark Estimate',
                              max_value=100, min_value=0)

    class Meta:
        model = Result
        fields = ('exam', 'mark')

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super(ViewMarksForm, self).__init__(*args, **kwargs)
        self.fields['mark'].widget = forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'id': 'markShow'})
        groupexams = query.examIDsinGroup(self.group)
        self.fields['exam'].queryset = Exam.objects.filter(pk__in=groupexams)

        for fieldname in ['mark', ]:
            self.fields[fieldname].help_text = None

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(label='Group name', max_length=100)

    class Meta:
        model = Group
        fields = ('group_name')

    def __init__(self, *args, **kwargs):
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_name'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'group_name'})
