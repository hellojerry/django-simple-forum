from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^compose/(?P<pk>\d+)/$', 'directmessages.views.compose', name='compose'),
    url(r'^inbox/(?P<slug>[-\w]+)/$', 'directmessages.views.inbox', name='inbox'),
    url(r'^outbox/(?P<slug>[-\w]+)/$', 'directmessages.views.outbox', name='outbox'),
    url(r'^conversation/(?P<pk>\d+)/$', 'directmessages.views.view_conversation', name='conversation'),
)