from django.test import TestCase, RequestFactory
import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from .views import ForumIndexView, ForumView, ReplyFormView
from .models import Forum, Thread, Post, ForumCategory
from .forms import PostForm, EMPTY_ITEM_ERROR
from profiles.models import Profile

from pizza.testutils import create_keyed_thread, post_invalid_thread_input, create_profile, \
                            create_post, create_forum, create_named_thread



class ForumIndexViewTest(TestCase):
    
    
    def test_forum_list_view_calls_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'index.html')
        
        
        
class ForumModelTest(TestCase):
    
    def test_get_absolute_url(self):
        forum = create_forum()
        self.assertEqual(forum.get_absolute_url(), '/forums/forum/%d/' % forum.id)
        
    def test_get_last_post(self):    
        thread = create_keyed_thread()
        profile = create_profile()
        post = create_post(profile, thread)
        post2 = create_post(profile, thread)
        self.assertEqual(post2, thread.forum.get_last_post())

class ThreadModelTest(TestCase):
    
    def test_get_absolute_url(self):
        thread = create_keyed_thread()
        self.assertEqual(thread.get_absolute_url(), '/forums/thread/%d/' % thread.id)
        
    
    def test_ordered_by_last_Postreverse(self):

        thread1 = create_keyed_thread()
        post = Post.objects.create(thread=thread1, author=thread1.creator)
        thread2 = Thread.objects.create(forum=thread1.forum, creator=thread1.creator)
        post2 = Post.objects.create(thread=thread2, author=thread1.creator)
        self.assertEqual(thread1, Thread.objects.all()[1])
        self.assertEqual(thread2, Thread.objects.all()[0])
        
    def test_get_last_post(self):
        thread = create_keyed_thread()
        profile = create_profile()
        post1 = create_post(profile, thread)
        post2 = create_post(profile, thread)
        self.assertEqual(post2, thread.get_last_post())
    
class PostModelTest(TestCase):
    
    def test_ordered_by_created(self):
        thread = create_keyed_thread()
        
        post1 = Post.objects.create(thread_id=thread.id, author=thread.creator)
        post2 = Post.objects.create(thread_id=thread.id, author=thread.creator)
        self.assertEqual(post1, Post.objects.all()[0])
        self.assertEqual(post2, Post.objects.all()[1])

    def test_get_absolute_url(self):
        thread = create_keyed_thread()
        user = User.objects.create()
        post = Post.objects.create(thread_id=thread.id, author=user)
        self.assertEqual(post.get_absolute_url(), '/forums/single_post/%d/' % post.id)
        
class ForumViewTest(TestCase):


    def test_if_view_calls_keyed_objects(self):

        thread1 = create_keyed_thread()
        thread2 = Thread.objects.create(forum=thread1.forum, creator=thread1.creator)
        response = self.client.get('/forums/forum/%d/' % thread1.forum.id)
        self.assertIn(thread1, list(response.context['object_list']))
        self.assertIn(thread2, list(response.context['object_list']))
        
        
    def test_if_view_calls_forum_object(self):
        forum = create_forum()
        response = self.client.get('/forums/forum/%d/' % forum.id)
        self.assertEquals(response.context['forum'], forum)
        
    def test_if_view_calls_invalid_objects(self):
        forum2 = create_forum()
        thread = create_keyed_thread()
        response = self.client.get('/forums/forum/%d/' % forum2.id)
        
        self.assertNotIn(thread, list(response.context['object_list']))       

class ThreadViewTest(TestCase):
    
    def test_Postlist_view_calls_correct_template(self):
        thread = create_keyed_thread()
        response = self.client.get('/forums/thread/%d/' % thread.id)
        self.assertTemplateUsed(response, 'thread.html')
    
    def test_if_view_calls_keyed_posts_in_order(self):
        thread = create_keyed_thread()
        response = self.client.get('/forums/thread/%d/' % thread.id)
        self.assertEquals(list(response.context['object_list']), [])
        
        author = User.objects.create()
        post1 = Post.objects.create(thread_id=thread.id, author=author)
        post2 = Post.objects.create(thread_id=thread.id, author=author)
        response = self.client.get('/forums/thread/%d/' % thread.id)
        self.assertIn(post1, list(response.context['object_list']))
        self.assertEqual(post1, list(response.context['object_list'])[0])
        
    def test_if_view_displays_form(self):
        thread = create_keyed_thread()
        form = PostForm
        response = self.client.get('/forums/thread/%d/' % thread.id)
        self.assertEqual(form, response.context['form'])


class SinglePostViewTest(TestCase):
    
    def test_single_post_view_calls_correct_template(self):
        thread = create_keyed_thread()
        user = User.objects.create()
        post = Post.objects.create(thread_id=thread.id,author=user)
        response = self.client.get('/forums/single_post/%d/' % post.id)
        self.assertTemplateUsed(response, 'single_post.html')
        
    def test_if_view_calls_single_keyed_post(self):
        thread = create_keyed_thread()
        user = User.objects.create()
        post = Post.objects.create(thread_id=thread.id,author=user)
        response = self.client.get('/forums/single_post/%d/' % post.id)
        self.assertEqual(post, response.context['object'])
        
        
    #this is showing an unbound form at the test client level, but it's the same form.     
    #def test_if_view_shows_form(self):
    #    thread = create_keyed_thread()
    #    post = Post.objects.create(thread=thread,author=thread.creator)

    #   response = self.client.get('/forums/single_post/%d/' % post.id)

    #   self.assertEquals(response.context['form'],PostForm)


    def test_if_valid_edit_updates_object(self):
        thread1 = create_keyed_thread()
        thread2 = Thread.objects.create(forum=thread1.forum, creator=thread1.creator)
        post1 = Post.objects.create(thread_id=thread1.id,author=thread1.creator, text='1')
        post2 = Post.objects.create(thread_id=thread2.id, author=thread1.creator, text='1')
        self.client.post(
            '/forums/single_post/%d/' % post1.id,
            data={'text': 'hello'}
        )
        self.assertEqual(str(thread1.post_set.all()[0].text), 'hello')
        self.assertNotEqual(str(thread2.post_set.all()[0].text),'hello',)
        self.assertNotEqual(str(thread1.post_set.all()[0].text), '1')
        

#class ReplyFormViewTest(TestCase):

#this was rewritten enough that the whole test needs to be dumped and redone.

        
###write tests for createthreadview, search
###

class SearchTest(TestCase):
    
    def test_if_search_grabs_threads(self):
        thread = create_named_thread()
        #the thread title from utils is 'hello'
        response = self.client.post(
            '/search/',
            data={'q':'hello'}
        )
    

        self.assertIn(thread, list(response.context['results']))
        
    def test_if_search_grabs_users(self):
        thread = create_named_thread()
        ##the username from utils is "fred"
        response = self.client.post(
            '/search/',
            data={'q':'fred'}
        )
        self.assertIn(thread.creator, list(response.context['results']))

    def test_if_search_grabs_posts(self):
        thread = create_named_thread()
        post_ = Post.objects.create(thread=thread, author=thread.creator, text='sledgehammer')
        response = self.client.post(
            '/search/',
            data={'q':'sledge'}
        )
        print list(response.context['results'])[2].text
        self.assertIn(post_, list(response.context['results']))
        

    
    

    

        