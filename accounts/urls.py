from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.AccountUpdateView.as_view(), name='user-update'),
)
