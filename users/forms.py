from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm



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
    
    
    
    
class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email} already exists')
        return email