from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email} not found')
        return email
    
    def clean_password(self):
        password = self.data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password\'s lenght must be greater than 8')
        return password


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
