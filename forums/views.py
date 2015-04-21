from django.contrib import messages
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .models import Forum, Thread, Post, ForumCategory
from .forms import PostForm, NewThreadForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from profiles.custom import active_and_login_required

import json
from itertools import chain


'''
rewrite tests for this first view
'''




class ForumIndexView(ListView):
    template_name = 'index.html'
    model = ForumCategory
    

    
class ForumView(SingleObjectMixin, ListView):
    template_name = 'forum.html'
    model = Thread
    paginate_by = 30
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Forum.objects.filter(id=kwargs.get('pk', None)))
        return super(ForumView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['forum'] = self.object
        return context
        
    def get_queryset(self):
        return self.object.thread_set.all()
    



class ThreadView(SingleObjectMixin, ListView):
    template_name = 'thread.html'
    model = Post
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        print request.GET
        self.object = self.get_object(queryset=Thread.objects.filter(id=kwargs.get('pk', None)))
        request.session['thread'] = self.object.id
        print 'thread id sent to session %s' % request.session['thread']
        return super(ThreadView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['thread'] = self.object
        context['form'] = PostForm
        return context
    
    def get_queryset(self):
        return self.object.post_set.all()



#rewrite these tests.

class ReplyFormView(FormView):
    form_class = PostForm
    template_name = 'thread.html'
    
    
    
    @method_decorator(active_and_login_required)
    def dispatch(self, *args, **kwargs):
        self.thread = Thread.objects.get(id=kwargs.get('pk', None))
        return super(ReplyFormView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.thread = self.thread
        post.text = form.cleaned_data['text']
        post.save()
        post.thread.save()
        
        self.success_url = '/forums/thread/%d/?page=last' % self.thread.id
        return super(ReplyFormView, self).form_valid(form)


    def form_invalid(self, form):
        return HttpResponseRedirect('/forums/thread/%d/?page=last' % self.thread.id)




class SinglePostView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'single_post.html'


class CreateThreadView(CreateView):
    form_class = NewThreadForm
    template_name = 'new_thread.html'
    
    @method_decorator(active_and_login_required)
    def dispatch(self, *args, **kwargs):
        self.forum = Forum.objects.get(id=kwargs.get('pk', None))
        return super(CreateThreadView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['forum'] = self.forum
        return context    
    
    
    
    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        
        thread = Thread(
            forum_id=self.forum.id,
            creator=user,
            title=form.cleaned_data['title']
        )
        post.author = user
        post.text = form.cleaned_data['text']
        thread.save()
        post.thread = thread
        
        post.save()
        
        
        self.success_url = reverse('forums:thread', args=[thread.id])
        return super(CreateThreadView, self).form_valid(form)


    
def quote(request, pk):
    if request.method == 'GET':
        post = Post.objects.get(id=pk)
        text = str(post.text)
        author = str(post.author)
        data = json.dumps({
            'text':text,
            'author': author,
        })

        return HttpResponse(data, content_type='application/json')


def search(request):
    try:
        q = request.GET.get('q', '')
    except:
        q = False
        
    user_queryset = User.objects.filter(
        Q(username__icontains=q)
    )
    thread_queryset = Thread.objects.filter(
        Q(title__icontains=q)
    )
    post_queryset = Post.objects.filter(
        Q(text__icontains=q)
    )
    results = list(chain(user_queryset, thread_queryset, post_queryset))
                   
    if q:
        query = 'Your search for %s returned the following results:' % q
    else:
        query = None
        
    template = 'search.html'
    context = {
        'q':q,
        'query': query,
        'results': results,
    }
    return render(request, template, context)