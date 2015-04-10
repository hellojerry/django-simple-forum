from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from PIL import Image

from directmessages.models import DirectMessage, MessageChain


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=25, blank=True, null=True)
    ##set this up as a defaultable
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
    '''
    def get_favorite_forum(self):
        for post in self.user.post_set.all():
    
    def get_favorite_thread(self):
    '''

    def get_all_profiles(self):
        return User.objects.all().order_by('username')
    
    def get_sent_messages(self):
        return DirectMessage.objects.filter(sender=self.user)
    
    def get_received_messages(self):
        return DirectMessage.objects.filter(recipient=self.user)
    
    
    
    def __unicode__(self):
        return '%s' % self.user.username
    

    