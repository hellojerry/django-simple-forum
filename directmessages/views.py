from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from .models import DirectMessage, MessageChain
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.
'''
test these
'''

class InboxView(ListView):
    template_name = 'inbox.html'
    model = DirectMessage
    '''
    @login_required
    def get_dispatch
    
    queryset =
    '''
    
class OutboxView(ListView):
    template_name = 'inbox.html'
    model = DirectMessage
    
    '''
    @login_required
    def get_dispatch
    
    queryset =
    '''

'''
test decorator, test incrementation, test the user check
'''

@login_required
def view_direct_message(request, dm_id):
    message = get_object_or_404(DirectMessage, id=dm_id)
    all_messages = DirectMessage.objects.filter(chain=message.chain)
    template = 'directmessages/templates/view.html'

    if message.sender != request.user and message.receiver != request.user:
        raise Http404
    
    if not message.read:
        message.read = True
        message.read_at = datetime.datetime.now()
        message.save()
    
    context = {
        'message': message,
        'all_messages': all_messages,
    }
    
    return render(request, template, context)
    