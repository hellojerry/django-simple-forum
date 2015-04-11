from django.test import TestCase, RequestFactory
import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from .views import ForumIndexView, ForumView, ReplyFormView
from .models import Forum, Thread, Post
from .forms import PostForm, EMPTY_ITEM_ERROR
from profiles.models import Profile


def create_keyed_thread():
    forum = Forum.objects.create()
    return Thread.objects.create(forum_id=forum.id)

def post_invalid_thread_input(self):
    thread = create_keyed_thread()
    return self.client.post(
        '/forums/thread/reply/%d/' % thread.id,
        data={'text':''}
    )


def create_profile():
    user = User.objects.create()
    profile = Profile.objects.create(user=user, slug='k')
    return profile


def create_post(profile, thread):
    return Post.objects.create(thread_id=thread.id, author=profile.user)

class ForumIndexViewTest(TestCase):
    
    
    def test_forum_list_view_calls_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'index.html')
        
        
        
class ForumModelTest(TestCase):
    
    def test_get_absolute_url(self):
        forum = Forum.objects.create()
        self.assertEqual(forum.get_absolute_url(), '/forums/forum/%d/' % forum.id)
        
    def test_get_last_post(self):
        forum = Forum.objects.create()
        thread = Thread.objects.create(forum_id=forum.id)
        profile = create_profile()
        post = create_post(profile, thread)
        post2 = create_post(profile, thread)
        self.assertEqual(post2, forum.get_last_post())

class ThreadModelTest(TestCase):
    
    def test_get_absolute_url(self):
        thread = create_keyed_thread()
        self.assertEqual(thread.get_absolute_url(), '/forums/thread/%d/' % thread.id)
        
    
    def test_ordered_by_last_Postreverse(self):
        forum = Forum.objects.create()
        thread1 = create_keyed_thread()
        thread2 = Thread.objects.create(forum_id=forum.id)
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
        forum = Forum.objects.create()
        thread = create_keyed_thread()
        user = User.objects.create()
        post1 = Post.objects.create(thread_id=thread.id, author=user)
        post2 = Post.objects.create(thread_id=thread.id, author=user)
        self.assertEqual(post1, Post.objects.all()[0])
        self.assertEqual(post2, Post.objects.all()[1])

    def test_get_absolute_url(self):
        thread = create_keyed_thread()
        user = User.objects.create()
        post = Post.objects.create(thread_id=thread.id, author=user)
        self.assertEqual(post.get_absolute_url(), '/forums/single_post/%d/' % post.id)
        
class ForumViewTest(TestCase):


    def test_if_view_calls_keyed_objects(self):
        forum = Forum.objects.create()
        response = self.client.get('/forums/forum/%d/' % forum.id)
        self.assertEquals(list(response.context['object_list']), [])

        thread1 = Thread.objects.create(forum_id=forum.id)
        thread2 = Thread.objects.create(forum_id=forum.id)
        response = self.client.get('/forums/forum/%d/' % forum.id)
        self.assertIn(thread1, list(response.context['object_list']))
        self.assertIn(thread2, list(response.context['object_list']))
        
        
    def test_if_view_calls_forum_object(self):
        forum = Forum.objects.create()
        response = self.client.get('/forums/forum/%d/' % forum.id)
        self.assertEquals(response.context['forum'], forum)
        
    def test_if_view_calls_invalid_objects(self):
        forum2 = Forum.objects.create()
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
        
    def test_if_view_shows_form(self):
        thread = create_keyed_thread()
        user = User.objects.create()
        post = Post.objects.create(thread_id=thread.id,author=user)

        response = self.client.get('/forums/single_post/%d/' % post.id)

        self.assertEquals(response.context['form'],PostForm)


    def test_if_valid_edit_updates_object(self):
        thread1 = create_keyed_thread()
        thread2 = create_keyed_thread()
        user = User.objects.create()
        post1 = Post.objects.create(thread_id=thread1.id,author=user, text='1')
        post2 = Post.objects.create(thread_id=thread2.id, author=user, text='1')
        self.client.post(
            '/forums/single_post/%d/' % post1.id,
            data={'text': 'hello'}
        )
        self.assertEqual(str(thread1.post_set.all()[0].text), 'hello')
        self.assertNotEqual(str(thread2.post_set.all()[0].text),'hello',)
        self.assertNotEqual(str(thread1.post_set.all()[0].text), '1')
        

class ReplyFormViewTest(TestCase):

    
    '''
    def test_if_valid_post_redirects_to_thread(self):
        
        thread = create_keyed_thread()
        thread2 = create_keyed_thread()
        user = User.objects.create()
        response = self.client.post(
            '/forums/thread/reply/%d/' % thread.id,
            data={'user':user, 'text': 'hello'}
        )
        self.assertRedirects(response, '/forums/thread/%d/' % thread.id)
        
        thread = create_keyed_thread()
        request = HttpRequest()
        request.user = User.objects.create()
        request.POST['text'] = 'a b c d'
        reply = ReplyFormView(request, thread)
        self.assertRedirects
        
        c = Client()
        thread = create_keyed_thread()
        author = User.objects.create()
        response = c.post('/forums/thread/reply/%d/' % thread.id, {'user':author, 'text':'a b c'})
        self.assertRedirects(response, '/forums/thread/%d/' %thread.id)
        '''

    def test_if_invalid_post_redirects_away(self):
        thread = create_keyed_thread()
        user = User.objects.create()
        response = self.client.post(
            '/forums/thread/reply/%d/' % thread.id,
            data={'': 'hello'}
        )
        self.assertRedirects(response, '/forums/thread/%d/' % thread.id)




    


    
    

    

        