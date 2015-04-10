from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from .models import DirectMessage, MessageChain
from .forms import ComposeForm, ReplyForm
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from profiles.models import Profile

@login_required
def compose(request, pk):
    template = 'compose.html'
    form = ComposeForm(request.POST or None)
    receiver = User.objects.get(id=pk)
    if form.is_valid():
        send_message = form.save(commit=False)
        send_message.sender = request.user
        send_message.sent = datetime.datetime.now()
        send_message.recipient = receiver
        send_message.chain = MessageChain.objects.create()
        send_message.save()
        messages.success(request, 'message sent')
        return HttpResponseRedirect(reverse('directmessages:outbox', args=[request.user.profile.slug]))
    
    context = {
        'form':form,
        'receiver': receiver,
    }
    return render(request, template, context)

@login_required
def inbox(request, slug):
    template = 'box.html'
    messages_ = DirectMessage.objects.filter(recipient=request.user)
    #variable is "messages_" to avoid clashing with django messages
    inbox = True
    profile = Profile.objects.get(slug=slug)
    if request.user.profile != profile:
        return Http404
    
    
    context = {
        'messages_': messages_,
        'inbox': inbox,
        'profile': profile,
    }
    
    return render(request, template, context)

@login_required
def outbox(request, slug):
    template = 'box.html'
    messages_ = DirectMessage.objects.filter(sender=request.user)
    outbox = True

    profile = Profile.objects.get(slug=slug)
    if request.user.profile != profile:
        return Http404
    
    context = {
        'messages_':messages_,
        'outbox': outbox,
        'profile': profile,
    }
    return render(request, template, context)

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

@login_required
def view_conversation(request, pk):
    template = 'chain.html'
    chain = MessageChain.objects.get(id=pk)

    form = ReplyForm(request.POST or None)
    
    context = {
        'chain': chain,
        'form': form,
    }
    return render(request, template, context)
    
    