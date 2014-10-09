from django.conf.urls import patterns, url
from clients.views import teachers as views


urlpatterns = patterns('',

    url(r'^$', views.KlassListView.as_view(), name='klass-list'),

    url(r'^(?P<pk>\d+)/iniciar/$', views.KlassStartView.as_view(), name='klass-start'),
    url(r'^(?P<pk>\d+)/iniciada/$', views.KlassDetailView.as_view(
        template_name='teachers/clients/klass_started.html'), name='klass-started'),

    url(r'^(?P<pk>\d+)/$', views.KlassDashboardView.as_view(), name='klass-dashboard'),
    url(r'^(?P<pk>\d+)/performance/$', views.KlassPerformanceView.as_view(), name='klass-performance'),

    url(r'^(?P<pk>\d+)/senhas/$', views.PasswdUpdateView.as_view(), name='passwd-update'),
    url(r'^(?P<pk>\d+)/senhas/ok/$', views.KlassDetailView.as_view(
        template_name='teachers/clients/passwd_update_done.html'), name='passwd-updated'),
    url(r'^(?P<pk>\d+)/senhas/imprimir/$', views.PasswdListView.as_view(), name='passwd-list'),

    url(r'^(?P<pk>\d+)/auto-reset-passwords/$', views.KlassAutoResetPasswordsView.as_view(), name='klass-auto-reset-passwords'),
    url(r'^(?P<pk>\d+)/reconfigurar/$', views.KlassRescheduleView.as_view(), name='klass-reschedule'),

    url(r'^(?P<pk>\d+)/agenda/$', views.KlassScheduleView.as_view(), name='initial-klass-schedule'),
    url(r'^(?P<pk>\d+)/agenda/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.KlassScheduleView.as_view(), name='klass-schedule'),
    url(r'^(?P<pk>\d+)/agenda/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.KlassScheduleDetailView.as_view(), name='klass-schedule-detail'),


)
