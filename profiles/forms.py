from django import forms
from profiles.models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'slug', 'is_active', 'name']
    

class LoginForm(AuthenticationForm):
    pass
    

class RegisterForm(UserCreationForm):

    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None




