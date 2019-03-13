from django import forms

class EnterBetsForm(forms.Form):
    user = forms.CharField(label='User name', max_length=100)
    exam = forms.CharField(label='Exam name', max_length=100)
    mark = forms.CharField(label='Guessed mark', max_length=100)

    def __init__(self, *args, **kwargs):
        super(EnterBetsForm, self).__init__(*args, **kwargs)

        for fieldname in ['user', 'exam', 'mark',]:
            self.fields[fieldname].help_text = None

        self.fields['user'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'user'})
        self.fields['exam'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'exam'})
        self.fields['mark'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'mark'})
