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
from .forms import EditProfileForm, LoginForm, RegisterForm
from django.utils.text import slugify

class ProfileView(DetailView):
    template_name = 'profile.html'
    model = Profile
    

class EditProfileView(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

'''
TEST THESE!
'''



def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_or_login(request):
    template = 'auth.html'
    
    register_form = RegisterForm(request.POST or None, initial={'form_tag':'register'})
    login_form = LoginForm(request.POST or None, initial={'form_tag':'login'})
    try:
        request.session['recent_auth']
        recent_auth = True
    except:
        recent_auth = False
    
    
    if request.method == 'POST':
        if request.POST['form_tag'] == 'register':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                form = register_form
                new_user = form.save(commit=False)
                slug = slugify(form.cleaned_data['username'])
        
                new_user.save()
                profile = Profile.objects.create(
                    user=new_user,slug=slug
                )
                
                username = form.cleaned_data['username']
                #password = form.cleaned_data['password']
                password = request.POST['password']
                user = authenticate(
                                username=username,
                                password=password,
                )
                print user
                login(request, user)
                request.session['recent_auth'] = True
                messages.success(request, 'Welcome!')
                return HttpResponseRedirect(reverse('register'))
            
        elif request.POST['form_tag'] == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                form = login_form
                password = form.cleaned_data['password']
                username = form.cleaned_data['username']
                user = authenticate(
                                username=username,
                                password=password,
                )
                login(request, user)
                messages.success(request, "Hello!")
                return HttpResponseRedirect(reverse('profiles:profile', args=[user.profile.slug]))
        
    context = {    
        'register_form': register_form,
        'login_form': login_form,
        'recent_auth': recent_auth,
    }
    
    return render(request, template, context)

###rewrite this to render two forms.

class RegisterView(FormView):
    template_name = 'auth.html'
    form_class = RegisterForm
    second_form_class = AuthenticationForm
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

