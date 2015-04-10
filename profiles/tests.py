from django.test import TestCase, RequestFactory
import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from forums.tests import create_keyed_thread
from forums.models import Post, Thread

from profiles.models import Profile
from profiles.forms import RegisterForm, LoginForm, EditProfileForm
## replace this with the get_user_model() once profiles are set up.
from django.contrib.auth.models import User

def create_profile():
    user = User.objects.create()
    profile = Profile.objects.create(user=user, slug='k')
    return profile

def create_post(profile, thread):
    return Post.objects.create(thread_id=thread.id, author=profile.user)


class UserProfileModelTest(TestCase):
    
    def test_get_absolute_url(self):
        profile = create_profile() 
        self.assertEqual(profile.get_absolute_url(), '/profiles/%s/' % profile.slug)
    

    def test_num_posts(self):
        profile = create_profile()
        thread = create_keyed_thread()
        post = create_post(profile, thread)
        self.assertEqual(profile.get_num_posts(), 1)
        
        

    def test_get_last_five_posts(self):
        profile = create_profile()
        thread = create_keyed_thread()
        post1 = create_post(profile, thread)
        post2 = create_post(profile, thread)
        post3 = create_post(profile, thread)
        post4 = create_post(profile, thread)
        post5 = create_post(profile, thread)
        self.assertIn(post1, profile.get_last_five_posts())
        self.assertIn(post2,profile.get_last_five_posts())
        self.assertIn(post3,profile.get_last_five_posts())
        self.assertIn(post4,profile.get_last_five_posts())
        self.assertIn(post5,profile.get_last_five_posts())


##test the two "favorites" querysets
    '''
    def test_get_favorite_forum(self):
        
    def test_get_favorite_thread(self):
    '''


class ProfileViewTest(TestCase):
    
    def test_profile_view_calls_correct_template(self):
        profile = create_profile()
        response = self.client.get('/profiles/%s/' % profile.slug )
        self.assertTemplateUsed(response, 'profile.html')
    
##test the profile update form
'''
ClassProfileUpdateFormTest(TestCase):

'''
    


class RegistrationTest(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    
    def test_registration_alls_correct_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'register.html')
        
    def test_register(self):
        response = self.client.post(
            '/register/',{
            'username': 'name',
            'password': 'password',
            'password2': 'password',
            'email': 'a@b.com',})
        self.assertEqual(response.status_code, 200)
    
        
class RegisterFormTest(TestCase):
    
    def test_form_throws_error_on_password_mismatch(self):
        form = RegisterForm(data={
            'username': 'name',
            'password': 'password',
            'password2': 'abcd',
            'email': 'a@b.com',
           
        })
        self.assertFalse(form.is_valid())
        
    def test_form_throws_error_on_used_email(self):
        old_user = User.objects.create(
            username='username',
            email='a@b.com',
        )
        form = RegisterForm(data={
            'username': 'name',
            'password': 'password',
            'password2': 'password',
            'email': 'a@b.com',            
        })
        self.assertFalse(form.is_valid())
        
    def test_form_throws_error_on_used_name(self):
        old_user = User.objects.create(
            username='name',
            email='a@c.com',
        )
        form = RegisterForm(data={
            'username': 'name',
            'password': 'password',
            'password2': 'password',
            'email': 'a@b.com',            
        })
        self.assertFalse(form.is_valid())
        
