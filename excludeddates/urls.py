from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

import views


perm_dec = permission_required('excludeddates.change_systemdate')


urlpatterns = patterns('',
    url(r'^$', perm_dec(views.SystemArchiveView.as_view()), name='system-archive'),
    url(r'^toggle/$', perm_dec(views.SystemToggleView.as_view()), name='system-toggle'),

    url(r'^client/$', views.ClientDisambiguationView.as_view(), name='client-disambiguation'),
    url(r'^client/(?P<pk>\d+)/$', views.ClientArchiveView.as_view(), name='client-archive'),
    url(r'^client/(?P<pk>\d+)/toggle/$', views.ClientToggleView.as_view(), name='client-toggle'),

    url(r'^teacher/$', views.TeacherDisambiguationView.as_view(), name='teacher-disambiguation'),
    url(r'^teacher/(?P<pk>\d+)/$', views.TeacherArchiveView.as_view(), name='teacher-archive'),
    url(r'^teacher/(?P<pk>\d+)/toggle/$', views.TeacherToggleView.as_view(), name='teacher-toggle'),
)
