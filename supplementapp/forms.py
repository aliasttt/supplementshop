from django import forms  
from .models import *
from django.contrib.auth.hashers import make_password

class Contactusform(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone = forms.CharField()
    subject = forms.CharField(max_length=20)
    text = forms.CharField(widget=forms.Textarea)




class RegisterForm(forms.ModelForm):
    class Meta:
        model = RegisterModel
        fields = ['name', 'lastname', 'email', 'password', 'phone']
    
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}), max_length=128)


    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your phone number'}), max_length=11)

  
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if email and RegisterModel.objects.filter(email=email).exists():
    #         raise forms.ValidationError("This email is already registered.")
    #     return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])  # هش کردن رمز عبور
        if commit:
            user.save()
        return user
    
