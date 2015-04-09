from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from precise_bbcode.fields import BBCodeTextField

class MessageChain(models.Model):
    started = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    
    def __unicode__(self):
        return str(self.id)
    

'''
test this
'''

class DirectMessageManager(models.Manager):
    def get_num_unread_messages(self, user):
        return super(DirectMessageManager, self).filter(read=False).filter(receiver=user).count()
    
    
class DirectMessage(models.Model):
    subject = models.CharField(max_length=100)
    text = BBCodeTextField()
    sender = models.ForeignKey(User, related_name='sent_direct_messages')
    recipient = models.ForeignKey(User, related_name='received_direct_messages')
    sent = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    read_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='parent_message')
    replied = models.BooleanField(default=False)
    chain = models.ForeignKey(MessageChain)
    
    objects = DirectMessageManager()
    
    def __unicode__(self):
        return 'subject: %s, sender: %s' % (self.subject, self.sender)
    
    class Meta:
        ordering = ['sent']
        
    def get_absolute_url(self):
        return reverse('view_direct_message', kwargs={'dm_id': self.id})
    