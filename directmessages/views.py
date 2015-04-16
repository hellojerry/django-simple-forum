from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404

from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from profiles.models import Profile
from .models import DirectMessage, MessageChain
from .forms import ComposeForm, MessageReplyForm

import json


@login_required
def compose(request, pk):
    template = 'compose.html'
    form = ComposeForm(request.POST or None)
    receiver = User.objects.get(id=pk)
    if form.is_valid():
        send_message = form.save(commit=False)
        send_message.sender = request.user
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
def view_conversation(request, pk):
    template = 'chain.html'
    chain = MessageChain.objects.get(id=pk)
    other_user = None
    
    for message_ in chain.directmessage_set.all():
        if request.user != message_.sender:
            other_user = message_.sender
            break
        elif request.user != message_.recipient:
            other_user = message_.recipient
            break

    form = MessageReplyForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            reply_message = form.save(commit=False)
            reply_message.subject = chain.directmessage_set.all()[0].subject
            reply_message.sender = request.user
            reply_message.recipient = other_user
            reply_message.chain = chain
            for i in chain.directmessage_set.filter(recipient=request.user):
                i.replied = True
                i.save()
            
            reply_message.save()
            
            return HttpResponseRedirect(reverse('directmessages:conversation', args=[pk]))
    
    context = {
        'chain': chain,
        'form': form,
        'other_user': other_user,
    }
    return render(request, template, context)
    
def quote(request, pk):
    if request.method == 'GET':
        message = DirectMessage.objects.get(id=pk)
        text = str(message.text)
        sender = str(message.sender)
        data = json.dumps({
            'text':text,
            'sender': sender,
        })

        return HttpResponse(data, content_type='application/json')

