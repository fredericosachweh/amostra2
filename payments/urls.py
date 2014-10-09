from django.conf.urls import patterns, url
from payments import views


urlpatterns = patterns('',

    url(r'^(?P<contract_pk>\d+)/$', views.PaymentListView.as_view(), name='payment-list'),
    url(r'^pagamento/(?P<pk>\d+)/$', views.PaymentDetailView.as_view(), name='payment-detail'),
    url(r'^pagamento/(?P<pk>\d+)/imprimir/$', views.print_payment, name='payment-print'),
)
