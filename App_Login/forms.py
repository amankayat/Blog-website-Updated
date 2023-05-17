
from dataclasses import field
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile
class signupform(UserCreationForm):
    email  = forms.EmailField(label="Email Address",widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    password1= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
        
        
        }

class UserProfileChange(UserChangeForm):
    class Meta:
        model = User
        fields=('username','email','first_name','last_name','password')

class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic',]