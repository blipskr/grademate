from django import forms
from models import Bet, Result
from django.contrib.auth.models import User


class EnterBetForm(forms.ModelForm):

    class Meta:
        model = Bet
        fields = ('exam', 'target', 'guess_mark', 'user')

    def __init__(self, *args, **kwargs):
        super(EnterBetForm, self).__init__(*args, **kwargs)



class UpdateBetForm(forms.Form):
    mark = forms.IntegerField(label='', max_value=100, min_value=0)

    class Meta:
        model = Bet
        fields = ('exam', 'target', 'guess_mark',)

    def __init__(self, *args, **kwargs):
        super(UpdateBetForm, self).__init__(*args, **kwargs)

        for fieldname in ['mark',]:
            self.fields[fieldname].help_text = None

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
