from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'first_name', 'last_name',]:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input'})
        for fieldname in ['password1', 'password2',]:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget = forms.PasswordInput(attrs={'class' : 'mdl-textfield__input'})

        self.fields['email'].widget = forms.EmailInput(attrs={'class' : 'mdl-textfield__input'})


class LoginForm(AuthenticationForm):
        class Meta:
            model = User
            fields = ('username', 'password')

        def __init__(self, *args, **kwargs):
            super(LoginForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input'})
            self.fields['password'].widget = forms.PasswordInput(attrs={'class' : 'mdl-textfield__input'})
