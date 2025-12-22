from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
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
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 bg-black/60 border border-purple-700/50 rounded-lg text-purple-200 placeholder-purple-400 focus:ring-2 focus:ring-purple-500 focus:outline-none shadow-inner shadow-purple-900/40",
            "placeholder": "Enter Password"
        }),
        label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 bg-black/60 border border-purple-700/50 rounded-lg text-purple-200 placeholder-purple-400 focus:ring-2 focus:ring-purple-500 focus:outline-none shadow-inner shadow-purple-900/40",
            "placeholder": "Confirm Password"
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "w-full px-3 py-2 bg-black/60 border border-purple-700/50 rounded-lg text-purple-200 placeholder-purple-400 focus:ring-2 focus:ring-purple-500 focus:outline-none shadow-inner shadow-purple-900/40",
                "placeholder": "Enter Username"
            }),
            'first_name': forms.TextInput(attrs={
                "class": "w-full px-3 py-2 bg-black/60 border border-purple-700/50 rounded-lg text-purple-200 placeholder-purple-400 focus:ring-2 focus:ring-purple-500 focus:outline-none shadow-inner shadow-purple-900/40",
                "placeholder": "Enter First Name"
            }),
            'last_name': forms.TextInput(attrs={
                "class": "w-full px-3 py-2 bg-black/60 border border-purple-700/50 rounded-lg text-purple-200 placeholder-purple-400 focus:ring-2 focus:ring-purple-500 focus:outline-none shadow-inner shadow-purple-900/40",
                "placeholder": "Enter Last Name"
            }),
            'email': forms.EmailInput(attrs={
                "class": "w-full px-3 py-2 bg-black/60 border border-purple-700/50 rounded-lg text-purple-200 placeholder-purple-400 focus:ring-2 focus:ring-purple-500 focus:outline-none shadow-inner shadow-purple-900/40",
                "placeholder": "Enter Email"
            }),
        }
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


class LoginForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        input_class = (
            "w-full px-3 py-2 bg-black/60 border border-purple-700/60 "
            "rounded-md text-purple-200 placeholder-purple-400 "
            "focus:ring-2 focus:ring-purple-500 focus:outline-none"
        )

        # Add classes to username
        self.fields['username'].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter Username",
        })

        # Add classes to password
        self.fields['password'].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter Password",
        })


class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role" 
    )
    
class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            'permissions': forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2"
            }),
        }
        labels = {
            'permissions': 'Assign Permissions'
        }
