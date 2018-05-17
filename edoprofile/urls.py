from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^login/$', views.RegLoginView.as_view(), name='login'),
    url(r'^login/$', views.regLogin, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
