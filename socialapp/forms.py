from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from socialapp.models import UserProfile

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user','following','block')

        widgets={
                    "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
                 }