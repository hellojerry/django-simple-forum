from django.db import models

from django.core.urlresolvers import reverse

#uncomment this when profiles app is complete.
#from django.contrib.auth import get_user_model
#User = get_user_model()
from django.contrib.auth.models import User
from precise_bbcode.fields import BBCodeTextField

'''
class ForumCategory(models.Model):
    title = models.CharField(max_length=100)
    
    
    def __unicode__(self):
        return self.title
'''




class Forum(models.Model):
    title = models.CharField(max_length=100)
    #moderators = models.ManyToManyField(UserProfile)
    
    #get rid of these and replay with FK to Category
    GENERAL = 'GENERAL'
    ENTERTAINMENT = 'ENTERTAINMENT'
    WORK = 'WORK'
    FORUM_GROUPS = (
        (GENERAL,'GENERAL'),
        (ENTERTAINMENT,'ENTERTAINMENT'),
        (WORK,'WORK'),
    )
    forum_group = models.CharField(max_length=30, choices=FORUM_GROUPS, default=ENTERTAINMENT)
    
    #category = models.ForeignKey(ForumCategory)
    is_active = models.BooleanField(default=True)
    
    
    def get_last_post(self):
        return self.thread_set.all().latest('last_post').post_set.all().latest('created')
    
    def get_absolute_url(self):
        return reverse('forums:single_forum', args=[self.id])
    
    def __unicode__(self):
        return str(self.id)


class Thread(models.Model):
    title = models.CharField(max_length=100, default='')
    forum = models.ForeignKey(Forum)
    creator = models.ForeignKey(User, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_post = models.DateTimeField(auto_now_add=False, auto_now=True)

    
    class Meta:
        ordering = ['-last_post']
    
    
    def get_last_post(self):
        return self.post_set.all().latest('created')

    def num_replies(self, ):
        return self.post_set.all().count() - 1

    
    def get_absolute_url(self):
        return reverse('forums:thread', args=[self.id])
    
    

    
    
    def __unicode__(self):
        return self.title
    
class Post(models.Model):
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User)
    text = BBCodeTextField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    edited = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    class Meta:
        ordering = ['created']
    
    def get_absolute_url(self):
        return reverse('forums:single_post', args=[self.id])
    
    
    def __unicode__(self):
        return str(self.author)