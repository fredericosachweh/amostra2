from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^p(?P<pk>\d+)/$', views.ProgramUsageLoginView.as_view(), name='klass-login'),
)
