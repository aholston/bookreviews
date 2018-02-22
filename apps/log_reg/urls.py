from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)/$', views.user),
    url(r'^viewbook/(?P<id>\d+)/$', views.viewbook),
    url(r'^addbook$', views.addbook),
    url(r'^addreview$', views.addreview),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^register$', views.register),
    url(r'^$', views.index)
]
