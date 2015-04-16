from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from precise_bbcode.fields import BBCodeTextField

class MessageChain(models.Model):
    started = models.DateTimeField(auto_now_add=True, auto_now=False)
    

    
    def __unicode__(self):
        return str(self.id)
    
"""
test the views
"""

    
    
class DirectMessage(models.Model):
    subject = models.CharField(max_length=100)
    text = BBCodeTextField()
    sender = models.ForeignKey(User, related_name='sent_direct_messages')
    recipient = models.ForeignKey(User, related_name='received_direct_messages')
    sent = models.DateTimeField(auto_now_add=True, auto_now=False)
    replied = models.BooleanField(default=False)
    chain = models.ForeignKey(MessageChain)
    
    
    def __unicode__(self):
        return 'subject: %s, sender: %s' % (self.subject, self.sender)
    
    class Meta:
        ordering = ['sent']
        
    