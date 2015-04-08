from django import forms
from profiles.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
    

class LoginForm(AuthenticationForm):
    
    '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    form_tag = forms.CharField(widget=forms.HiddenInput())
    
    def clean(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']

        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('This password is incorrect.')
        return self.cleaned_data
    '''
class RegisterForm(UserCreationForm):
    
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None



'''    
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    form_tag = forms.CharField(widget=forms.HiddenInput())    
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'password', 'password2']:
            self.fields[fieldname].help_text = None
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('That username is taken!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('That email is taken!')  
        return email
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password == password2:
            final_password = make_password(password)
            del cleaned_data['password']
            del cleaned_data['password2']
            cleaned_data['password'] = final_password
            cleaned_data['password2'] = final_password
            
        if password != password2:
            self.errors['password'] = self.error_class(["The passwords don't match!"])
            del cleaned_data['password']
            del cleaned_data['password2']
            
        return cleaned_data
    
    def log_user_in(self, user):
        login(self.request, user)
    ##trying this out'''
'''    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        if commit:
            user.save()
            authenticate(username=user.username, password=user.password)
            log_user_in(user)
        return user
'''
