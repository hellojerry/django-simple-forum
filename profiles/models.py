from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from PIL import Image

from directmessages.models import DirectMessage, MessageChain


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=25, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)
    description = models.TextField(max_length=500, default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    
    
    def get_absolute_url(self):
        return reverse('profiles:profile', args=[self.slug])

    
    def get_num_posts(self):
        return self.user.post_set.all().count()
    def get_last_five_posts(self):
        return self.user.post_set.all().order_by('-id')[0:5]

#test these two querysets

    def get_favorite_thread(self):
        counter = {}
        max_count = 0
        for post in self.user.post_set.all():
             try:
                 counter[post.thread]
                 counter[post.thread] += 1
             except KeyError:
                 counter[post.thread] = 1
             if counter[post.thread] > max_count:
                 max_count = counter[post.thread]
                 favorite = post.thread
        if max_count == 0:
            favorite = None
        return favorite
    
    def get_favorite_forum(self):
        counter = {}
        max_count = 0
        for post in self.user.post_set.all():
            try:
                counter[post.thread.forum]
                counter[post.thread.forum] += 1
            except KeyError:
                counter[post.thread.forum] = 1
            if counter[post.thread.forum] > max_count:
                max_count = counter[post.thread.forum]
                favorite = post.thread.forum
        if max_count == 0:
            favorite = None
            
        return favorite

##trivial? maybe not test these    

    def get_all_profiles(self):
        return User.objects.all().order_by('username')
    
    def get_sent_messages(self):
        return DirectMessage.objects.filter(sender=self.user)
    
    def get_received_messages(self):
        return DirectMessage.objects.filter(recipient=self.user)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return '%s' % self.user.username
    

    