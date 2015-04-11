from django.conf.urls import patterns, include, url
from .views import ForumView, ThreadView, SinglePostView, ReplyFormView, CreateThreadView

urlpatterns = patterns('',

    url(r'^forum/(?P<pk>\d+)/$', ForumView.as_view(), name='single_forum'),
    url(r'^thread/(?P<pk>\d+)/$', ThreadView.as_view(), name='thread'),
    url(r'^thread/reply/(?P<pk>\d+)/$', ReplyFormView.as_view(), name='reply'),
    url(r'^single_post/(?P<pk>\d+)/$', SinglePostView.as_view(), name='single_post'),
    url(r'^forum/new_thread/(?P<pk>\d+)/$', CreateThreadView.as_view(), name='create_thread'),
)

