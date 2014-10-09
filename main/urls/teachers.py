from django.contrib import admin
from django.conf.urls import patterns, url, include

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^programas/', include('exercises.urls.teachers')),
    url(r'^', include('clients.urls.teachers')),
)
