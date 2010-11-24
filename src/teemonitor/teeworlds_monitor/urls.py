

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^servers/$', views.ServerListView.as_view(), name="server_list"),
    url(r'^server/(?P<pk>\d+)/$', views.ServerDetailView.as_view(), name="server_detail"),
    url(r'^version/(?P<version>.+)/$', views.VersionDetailView.as_view(), name="version_detail"),
    url(r'^match/(?P<pk>\d+)/$', views.MatchDetailView.as_view(), name="match_detail"),
    url(r'^player/(?P<pk>\d+)/$', views.PlayerDetailView.as_view(), name="player_detail"),
    url(r'^gametype/(?P<pk>\d+)/$', views.GameTypeDetailView.as_view(), name="gametype_detail"),
    url(r'^gamemap/(?P<pk>\d+)/$', views.GameMapDetailView.as_view(), name="gamemap_detail"),
    #(r'^/$', 'views.servers'),
)