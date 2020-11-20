from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

from .models import*

class UserLogin(forms.ModelForm):
    class Meta:
        model = Account
        fields=('account_name', 'password',)



        
     
 

   
    