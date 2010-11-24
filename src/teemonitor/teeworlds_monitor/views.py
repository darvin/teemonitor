from django.views.generic import DetailView, TemplateView, ListView
from models import Server, Player, Match, GameMap, GameType
from GChartWrapper.encoding import Encoder
class ServerListView(ListView):
    context_object_name = "server_list"
    model = Server

class ServerDetailView(DetailView):

    context_object_name = "server"
    model = Server

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)
        context['match'] = self.get_object().match_set.latest()
        context['players_scores'] = []
        e = Encoder("text")
        context['players_nums_data'] = e.encodedata( [d.data for d in self.get_object().nums_players.all()])
        context['players_nums_datetime'] = "one thow tree"
        for player in self.get_object().match_set.latest().players.all():
            player_name = player.name
            player_score = player.score_set.latest().data
            context['players_scores'].append((player_name, player_score))
        return context

class VersionDetailView(TemplateView):
    template_name = "teeworlds_monitor/version_detail.html"
    def get_context_data(self, **kwargs):
        context = super(VersionDetailView, self).get_context_data(**kwargs)
        context["version"] = kwargs["version"]
        return context
    
    
class MatchDetailView(DetailView):

    context_object_name = "match"
    model = Match

    def get_context_data(self, **kwargs):
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        context['players_scores']=[]
        for player in self.get_object().players.all():
            player_name = player.name
            player_score = player.score_set.latest().data
            context['players_scores'].append((player_name, player_score))

        return context

    
class PlayerDetailView(DetailView):

    context_object_name = "player"
    model = Player

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        return context
  
class GameMapDetailView(DetailView):

    context_object_name = "gamemap"
    model = GameMap

    def get_context_data(self, **kwargs):
        context = super(GameMapDetailView, self).get_context_data(**kwargs)
        return context
  
class GameTypeDetailView(DetailView):

    context_object_name = "gametype"
    model = GameType

    def get_context_data(self, **kwargs):
        context = super(GameTypeDetailView, self).get_context_data(**kwargs)
        return context
