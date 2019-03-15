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
        for fieldname in ['password1', 'password2',]:
            self.fields[fieldname].help_text = None

        self.fields['username'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'username'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'firstname'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'lastname'})

        self.fields['email'].widget = forms.EmailInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'email'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'password1'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'password2'})

class LoginForm(AuthenticationForm):
        class Meta:
            model = User
            fields = ('username', 'password')

        def __init__(self, *args, **kwargs):
            super(LoginForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input'})
            self.fields['password'].widget = forms.PasswordInput(attrs={'class' : 'mdl-textfield__input'})

class AccountEditForm(forms.ModelForm):
    password1 = forms.CharField(required = True, label="Password")
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name', 'email',]:
            self.fields[fieldname].help_text = None

        self.fields['first_name'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'username'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'firstname'})
        self.fields['email'].widget = forms.TextInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'lastname'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class' : 'mdl-textfield__input', 'id' : 'password1'})
