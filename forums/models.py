from django.db import models


from django.core.paginator import Paginator

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


from precise_bbcode.fields import BBCodeTextField


class ForumCategory(models.Model):
    title = models.CharField(max_length=100)
    
    
    def __unicode__(self):
        return self.title





class Forum(models.Model):
    title = models.CharField(max_length=100)
    #moderators = models.ManyToManyField(User, blank=True, null=True)
    
    category = models.ForeignKey(ForumCategory)
    is_active = models.BooleanField(default=True)
    custom_css = models.FileField(upload_to='forum_stylesheets/%Y/%m/%d/', blank=True, null=True)
    
    def get_last_post(self):
        return self.thread_set.all().latest('last_post').post_set.all().latest('created')
    
    def get_absolute_url(self):
        return reverse('forums:single_forum', args=[self.id])

    
    def get_most_popular_thread(self):
        counter = {}
        max_count = 0
        for thread in self.thread_set.all():
            counter[thread.id] = thread.count_all_posts()
            if counter[thread.id] > max_count:
                max_count = counter[thread.id]
                favorite = thread.id
        if max_count == 0:
            favorite = None
        return Thread.objects.get(id=favorite)
    
    def get_most_popular_thread_url(self):
        favorite = self.get_most_popular_thread().id
        return Thread.objects.get(id=favorite).get_absolute_url()
    
    
    def get_num_posts(self):
        postcount = []
        for thread in self.thread_set.all():
            postcount.append(thread.count_all_posts())
        return sum(postcount)
    
    
    
    
    
    def __unicode__(self):
        return self.title


class Thread(models.Model):
    title = models.CharField(max_length=100)
    forum = models.ForeignKey(Forum)
    creator = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_post = models.DateTimeField(auto_now_add=False, auto_now=True)

    
    class Meta:
        ordering = ['-last_post']
    
    
    def get_last_post(self):
        return self.post_set.all().latest('created')

    def num_replies(self, ):
        return self.post_set.all().count() - 1

    def count_all_posts(self):
        return self.post_set.all().count()
    
    def get_absolute_url(self):
        return reverse('forums:thread', args=[self.id])
    
    def get_last_30_posts(self):
        return self.post_set.all()[0:30]

    

    
    
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
    
    #for this redirect to work properly, the pagination number argument
    #in this function must match the paginate_by value in ThreadView.
        
    def link_to_post_in_thread(self):
        thread_posts = Post.objects.filter(thread_id=self.thread.id)
        paginator = Paginator(thread_posts, 10)
        target_page = None
        for page_number in range(1, paginator.num_pages+1):
            if self in paginator.page(page_number).object_list:
                target_page = page_number
                break
            else:
                pass
        if target_page != None:
            return '/forums/thread/%d/?page=%d' %(self.thread.id, target_page)
    
    
    
    def __unicode__(self):
        return str(self.author)