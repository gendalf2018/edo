from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DocListView.as_view(), name='doclist'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.EditorView.as_view(), name='editorurl'),
    url(r'^view/new/$', views.EditorNewView.as_view(), name='editornewurl'),
    url(r'^save/$', views.EditorSaveView.as_view(), name='editorsaveurl'),
    url(r'^groups/$', views.EditorGroupView.as_view(), name='editorgroups'),
    url(r'^users/$', views.EditorUserView.as_view(), name='editorusers'),
]
