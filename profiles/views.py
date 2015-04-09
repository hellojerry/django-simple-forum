from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.contrib import messages
from .models import Profile
from .forms import EditProfileForm, RegisterForm, LoginForm
#LoginForm,
from django.utils.text import slugify


    

class ProfileView(UpdateView):
    model = Profile
    template_name = 'profile.html'
    form_class = EditProfileForm




def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')






class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url='/'
    
    
    
    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        slug = slugify(self.request.POST['username'])
        profile = Profile.objects.create(
            user=new_user,slug=slug
        )
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)





class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    

