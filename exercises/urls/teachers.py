from django.conf.urls import patterns, url
from exercises import views


urlpatterns = patterns('',

    url(r'^(?P<pk>\d+)/$', views.ProgramUsageDetailView.as_view(), name='program-usage-detail'),
    url(r'^(?P<pk>\d+)/syllabus/$', views.SyllabusListView.as_view(), name='syllabus'),

)
