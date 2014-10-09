from django.conf.urls import patterns, url
from clients.views import managers as views


urlpatterns = patterns('',

    # Contracts
    url(r'^$', views.ContractListView.as_view(), name='contract-list'),
    url(r'^(?P<pk>\d+)/$', views.ContractDetailView.as_view(), name='contract-detail'),

    # Contract classes
    url(r'^(?P<contract_pk>\d+)/classes/create/$', views.KlassCreateView.as_view(), name='klass-create'),
    url(r'^(?P<contract_pk>\d+)/classes/(?P<pk>\d+)/$', views.ContractKlassDetailView.as_view(), name='klass-detail'),
    url(r'^(?P<contract_pk>\d+)/classes/(?P<pk>\d+)/update/$', views.KlassUpdateView.as_view(), name='klass-update'),
    url(r'^(?P<contract_pk>\d+)/classes/(?P<pk>\d+)/delete/$', views.KlassDeleteView.as_view(), name='klass-delete'),
    # XXX url(r'^(?P<contract_pk>\d+)/classes/$', views.KlassListView.as_view(), name='klass-list'),

    # Teachers management
    url(r'^professores/$', views.TeacherListView.as_view(), name='teacher-list'),
    url(r'^professores/create/$', views.TeacherCreateView.as_view(), name='teacher-create'),
    url(r'^professores/(?P<pk>\d+)/$', views.TeacherDetailView.as_view(), name='teacher-detail'),
    url(r'^professores/(?P<pk>\d+)/update/$', views.TeacherUpdateView.as_view(), name='teacher-update'),
    url(r'^professores/(?P<pk>\d+)/delete/$', views.TeacherDeleteView.as_view(), name='teacher-delete'),
    url(r'^professores/(?P<pk>\d+)/cant-delete/$', views.TeacherCantDeleteView.as_view(), name='teacher-cant-delete'),

)
