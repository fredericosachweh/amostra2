from django.contrib import admin
from django.conf.urls import patterns, url, include
from clients.views.students import KlassAccessView, KlassLoginView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^acessar-turma/$', KlassAccessView.as_view(), name='klass-access'),
    url(r'^tarefas/', include('exercises.urls.students')),
    url(r'^(?P<key>\w+)/$', KlassLoginView.as_view(), name='klass-login'),
)
