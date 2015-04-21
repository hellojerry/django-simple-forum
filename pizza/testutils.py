from forums.models import Forum, ForumCategory, Post, Thread
from django.contrib.auth.models import User
from profiles.models import Profile

from django.test import Client

def create_keyed_thread():
    user = User.objects.create(username='fred', password='password')
    c = Client()
    c.login(username='fred', password='password')
    category = ForumCategory.objects.create()
    forum = Forum.objects.create(category_id=category.id)
    return Thread.objects.create(forum_id=forum.id, creator=user)


def create_named_thread():
    user = User.objects.create(username='fred', password='password')
    c = Client()
    c.login(username='fred', password='password')
    category = ForumCategory.objects.create()
    forum = Forum.objects.create(category_id=category.id)
    return Thread.objects.create(forum_id=forum.id, creator=user, title='hello')

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

def create_forum():
    category = ForumCategory.objects.create()
    return Forum.objects.create(category=category)