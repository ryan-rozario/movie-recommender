import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms

from .models import Rating

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30 ,widget=forms.TextInput(attrs={'class':'input100', 'type':"text", 'name':'username', 'placeholder':'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input100', 'type':"text", 'name':'email', 'placeholder':'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100', 'type':"password", 'name':'password1', 'placeholder':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100', 'type':"password", 'name':'password2', 'placeholder':'Retype Password'}))

    def cleaned_password(self):
        if 'password1' in self.cleaned_data:
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Password does not match!')

    def cleaned_username(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        try:
            u_dup = User.objects.get(email=email)
            if u_dup.exists():
                raise forms.ValidationError('User already exists!')
            u_dup = User.objects.get(username=username)
            if u_dup.exists():
                raise forms.ValidationError('User already exists!')		
        except ObjectDoesNotExist:
            pass
