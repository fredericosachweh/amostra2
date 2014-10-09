from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from demonstrations.views import main, purchases


purchases_urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', purchases.StartView.as_view(), name='start'),
    url(r'^(?P<pk>\d+)/atualizar/$', purchases.ClientUpdateView.as_view(), name='client-update'),
    url(r'^(?P<pk>\d+)/contrato/$', purchases.ContractAgreeView.as_view(), name='contract-agree'),
    url(r'^(?P<pk>\d+)/contrato/imprimir/$', purchases.ContractPrintView.as_view(), name='contract-print'),
    url(r'^(?P<pk>\d+)/turmas/$', purchases.KlassesCreateView.as_view(), name='klasses-create'),
    url(r'^(?P<pk>\d+)/pagamento/$', purchases.PaymentView.as_view(), name='payment'),
)


urlpatterns = patterns('',
    url(r'^$', main.DemonstrationCreateView.as_view(), name='demo-create'),
    url(r'^pronto/$', TemplateView.as_view(template_name='demonstrations/demonstration_create_done.html'), name='demo-create-done'),
    url(r'^expirada/$', TemplateView.as_view(template_name='demonstrations/demonstration_expired.html'), name='demo-expired'),
    url(r'^(?P<pk>\d+)/programas/$', main.ProgramListView.as_view(), name='programs'),
    url(r'^(?P<pk>\d+)/$', main.DemonstrationStartView.as_view(), name='demo-start'),
    url(r'^(?P<pk>\d+)/tentativa/(?P<cat>\d+)/$', main.ChanceCreateView.as_view(), name='chance-create'),
    url(r'^(?P<pk>\d+)/tentativa/(?P<cat>\d+)/ok/$', main.ChanceDetailView.as_view(), name='chance-detail'),
    url(r'^(?P<pk>\d+)/done/$', main.DemonstrationDoneView.as_view(), name='demo-done'),
    url(r'^(?P<pk>\d+)/send/$', main.DemonstrationSendView.as_view(), name='demo-send'),

    url(r'^comprar/', include(purchases_urlpatterns, namespace='purchase')),
)
