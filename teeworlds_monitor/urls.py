

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^server/(?P<pk>\d+)/$', views.ServerDetailView.as_view()),
    (r'^version/(?P<version>.+)/$', views.VersionDetailView.as_view()),
    #(r'^/$', 'views.servers'),
)