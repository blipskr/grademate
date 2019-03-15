from django import forms
from models import Bet

class EnterBetForm(forms.Form):
    user = forms.CharField(label='User name', max_length=100)
    exam = forms.CharField(label='Exam name', max_length=100)
    mark = forms.IntegerField(label='Guessed mark', max_value=100, min_value=0)

    class Meta:
        model = Bet
        fields = ('bet_id', 'exam', 'user', 'target', 'guess_mark', 'win', )

    def __init__(self, *args, **kwargs):
        super(EnterBetForm, self).__init__(*args, **kwargs)

        for fieldname in ['user', 'exam', 'mark',]:
            self.fields[fieldname].help_text = None

        self.fields['user'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'user'})
        self.fields['exam'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'exam'})
        self.fields['mark'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'mark'})

class UpdateBetForm(forms.Form):
    mark = forms.IntegerField(label='', max_value=100, min_value=0)

    class Meta:
        model = Bet
        fields = ('bet_id', 'exam', 'user', 'target', 'guess_mark', 'win', )

    def __init__(self, *args, **kwargs):
        super(UpdateBetForm, self).__init__(*args, **kwargs)

        for fieldname in ['mark',]:
            self.fields[fieldname].help_text = None

        self.fields['mark'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'mark'})
