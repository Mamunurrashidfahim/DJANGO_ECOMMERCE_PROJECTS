from django import forms
from App_Login.models import User,Profile

from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude =('user',)

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("email","password1","password2",)

class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password')  
