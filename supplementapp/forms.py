from django import forms  
from .models import *


class Contactusform(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone = forms.CharField()
    subject = forms.CharField(max_length=20)
    text = forms.CharField(widget=forms.Textarea)
