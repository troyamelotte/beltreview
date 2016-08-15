from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.booksadd),
    url(r'^newbook$', views.newbook),
    url(r'^books/(?P<id>\d+)$', views.viewbook),
    url(r'^remove/(?P<id>\d+)$', views.removereview),
    url(r'^newreview/(?P<id>\d+)$', views.newreview),
    url(r'^users/(?P<id>\d+)$', views.account)
]
