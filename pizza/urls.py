from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from forums.views import ForumIndexView
from profiles.views import RegisterView

urlpatterns = patterns('',

    url(r'^$', ForumIndexView.as_view(), name='main'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', 'profiles.views.my_logout', name='logout'),
    url(r'^forums/', include('forums.urls', namespace='forums')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)