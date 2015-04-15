from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView, FormMixin
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.list import MultipleObjectMixin
from .models import Forum, Thread, Post, ForumCategory
from forums.forms import PostForm, NewThreadForm
from django.contrib import messages
from django.contrib.auth.models import User

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
    paginate_by = 5
    
    def get(self, request, *args, **kwargs):
        print request.GET
        #print vars(self.paginator_class._get_page_range)
        #print self.paginator_class._get_num_pages
        #print self.paginator_class._get_page_range
        #print self.paginator_class.page_range
        #print self.paginator_class
        self.object = self.get_object(queryset=Thread.objects.filter(id=kwargs.get('pk', None)))
        return super(ThreadView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['thread'] = self.object
        context['form'] = PostForm
        return context
    
    def get_queryset(self):
        return self.object.post_set.all()

'''
rewrite this to be its own page so that form_invalid will work properly.

grab a queryset of the last page's worth of posts.
'''


class ReplyFormView(FormView):
    form_class = PostForm
    template_name = 'thread.html'
    
    #add in the permissions decorator later
    
    
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        print self.request.POST
        self.thread = Thread.objects.get(id=kwargs.get('pk', None))
        return super(ReplyFormView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.thread = self.thread
        post.text = form.cleaned_data['text']
        post.save()
        post.thread.save()
        
        #self.success_url = reverse('forums:thread', args=[self.thread.id])
        self.success_url = HttpResponseRedirect('/forums/thread/%d/?page=last', self.thread.id)
        #self.success_url = reverse('forums:thread', args=[self.thread.id, self.page])
        #self.success_url = HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        return super(ReplyFormView, self).form_valid(form)


#TEST THIS!

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('forums:thread', args=[self.thread.pk]))


class SinglePostView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'single_post.html'


class CreateThreadView(CreateView):
    form_class = NewThreadForm
    template_name = 'new_thread.html'
    
    ##add in method decorator
    def dispatch(self, *args, **kwargs):
        self.forum = Forum.objects.get(id=kwargs.get('pk', None))
        return super(CreateThreadView, self).dispatch(*args, **kwargs)
    
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
        

