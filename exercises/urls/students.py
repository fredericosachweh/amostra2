from django.conf.urls import patterns, url
from exercises.views import main

# tarefas/
# tarefas/1/
# tarefas/1/exercicio-1/
# tarefas/1/tentativa-1/
# tarefas/1/fim/

urlpatterns = patterns('',

    url(r'^$', main.UserBatteriesListView.as_view(), name='user-battery-list'),
    url(r'^(?P<schedule>\d+)/$', main.UserBatteryStartView.as_view(), name='user-battery-start'),
    url(r'^(?P<user_battery>\d+)/exercicio-(?P<position>\d+)/$', main.ChanceCreateView.as_view(), name='chance-create'),
    url(r'^(?P<user_battery>\d+)/exercicio-(?P<position>\d+)/tentativa-(?P<number>\d+)/$', main.ChanceDetailView.as_view(), name='chance-detail'),
    url(r'^(?P<user_battery>\d+)/fim/$', main.UserBatteryDoneView.as_view(), name='user-battery-done'),

)
