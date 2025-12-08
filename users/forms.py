from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        
        for field in ['username','password1','password2']:
            self.fields[field].help_text = None


class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','confirm_password','email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        
        if email_exists:
            raise forms.ValidationError("Email Already Exists")
        return email    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")

        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*]', password):
            errors.append("Password must contain at least one special character (!@#$%^&*)")

        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Pasword did not matched")
        
        return cleaned_data
    
    def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data['password'])  # hash password
       if commit:
           user.save()
       return user