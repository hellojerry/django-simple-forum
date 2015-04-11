from django.conf.urls import patterns, include, url

from profiles.views import ProfileView, ProfileIndexView

urlpatterns = patterns('',

    url(r'^(?P<slug>[-\w]+)/$', ProfileView.as_view(), name='profile'),
    url(r'^$', ProfileIndexView.as_view(), name='profile_index'),
)