from django import forms
from models import Bet, Result
from django.contrib.auth.models import User
from models import Exam
import dbqueries as query



class EnterBetForm(forms.ModelForm):
    exam = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))
    target = forms.ModelChoiceField(queryset=User.objects.filter(pk=1))
    class Meta:
        model = Bet
        fields = ('exam', 'target', 'guess_mark',)

    def __init__(self, *args, **kwargs):
        global target
        self.group = kwargs.pop('group')
        super(EnterBetForm, self).__init__(*args, **kwargs)
        self.fields['guess_mark'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'guess_mark'})
        groupusers = query.userIDsinGroup(self.group)
        groupexams = query.examIDsinGroup(self.group)
        self.fields['target'].queryset = User.objects.filter(pk__in=groupusers)
        self.fields['exam'].queryset = Exam.objects.filter(pk__in=groupexams)

class UpdateBetForm(forms.Form):
    bet = forms.ModelChoiceField(queryset=Bet.objects.filter(pk=1))
    mark = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.myBets = kwargs.pop('bets')
        super(UpdateBetForm, self).__init__(*args, **kwargs)
        self.fields['bet'].queryset = self.myBets
        self.fields['mark'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'mark'})


class EnterMarksForm(forms.ModelForm):
    user = forms.CharField(label='Username', max_length=100)
    exam = forms.CharField(label='Exam', max_length=100)
    mark = forms.IntegerField(label='Mark Estimate', max_value=100, min_value=0)

    class Meta:
        model = Result
        fields = ('exam', 'user', 'mark')

    def __init__(self, *args, **kwargs):
        super(EnterMarksForm, self).__init__(*args, **kwargs)

        for fieldname in ['user', 'exam', 'mark',]:
            self.fields[fieldname].help_text = None

        self.fields['exam'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'exam'})
        self.fields['user'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'user'})
        self.fields['mark'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'mark'})
