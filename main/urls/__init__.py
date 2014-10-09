from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from accounts.views import LoginView
from exercises.views.admin import (CategoryFillView, CategoryDuplicateView,
                                   ChanceCreateView, ChanceDetailView,
                                   ProgramAuditView, ProgramReplaceView,
                                   ProgramUsageAuditView)
from clients.views import ClientsImportView, InvoiceDataView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^home/$', LoginView.as_view(), name='home'),
    url(r'^sair/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^recuperar-senha/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^recuperar-senha/ok/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^recuperar-senha/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^recuperar-senha/confirmar/ok/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    url(r'^$', TemplateView.as_view(template_name='soon_available.html'), name='soon-available'),
    url(r'^escolha-perfil/$', TemplateView.as_view(template_name='home_desambiguation.html'), name='home-desambiguation'),
    url(r'^saiba-mais/$', TemplateView.as_view(template_name='informations.html'), name='informations'),

    url(r'^conta/', include('accounts.urls', namespace='accounts')),

    url(r'^turmas/', include('main.urls.teachers', namespace='teacher')),
    url(r'^contratos/', include('main.urls.managers', namespace='manager')),

    url(r'^excludeddates/', include('excludeddates.urls', namespace='excludeddates')),
    url(r'^demonstracoes/', include('demonstrations.urls', namespace='demonstrations')),
    url(r'^financeiro/', include('payments.urls', namespace='payments')),

    # admin stuff urls
    url(r'^grappelli/', include('grappelli.urls')),

    # inaccessible class
    url(r'^turma-inacessivel/$', TemplateView.as_view(template_name='inaccessible_klass.html'), name='inaccessible-klass'),

    url(r'^newsletter.html$', TemplateView.as_view(template_name='newsletter.html'), name='newsletter'),

    url(r'^admin/exercises/exercise/(?P<pk>\d+)/view/$', ChanceCreateView.as_view(), name='admin-chance-create'),
    url(r'^admin/exercises/chance/(?P<pk>\d+)/view/$', ChanceDetailView.as_view(), name='admin-chance-detail'),
    url(r'^admin/exercises/category/(?P<pk>\d+)/fill-from-csv/$', CategoryFillView.as_view(), name='category-fill'),
    url(r'^admin/exercises/category/(?P<pk>\d+)/duplicate/$', CategoryDuplicateView.as_view(), name='category-duplicate'),
    url(r'^admin/exercises/program/(?P<pk>\d+)/batteries/$', ProgramAuditView.as_view(), name='program-audit'),
    url(r'^admin/exercises/program/(?P<pk>\d+)/replace/$', ProgramReplaceView.as_view(), name='program-replace'),
    url(r'^admin/exercises/programusage/(?P<pk>\d+)/detail/$', ProgramUsageAuditView.as_view(), name='programusage-audit'),
    url(r'^admin/clients/import/$', ClientsImportView.as_view(), name='clients-import'),
    url(r'^admin/clients/(?P<pk>\d+)/invoice-data/$', InvoiceDataView.as_view(), name='invoice-data'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('main.urls.students', namespace='student')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^docs/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.DOCS_ROOT, 'show_indexes': True}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    ) + urlpatterns
