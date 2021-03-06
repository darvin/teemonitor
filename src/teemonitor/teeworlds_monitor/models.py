from django.db import models
from libs.tw_api import get_server_info, get_all_servers
from django_statisticaldata.models import StatisticalData
import datetime
########################################################################

from django.conf import settings
class ServerManager(models.Manager):
    def refresh(self):
        delta = (datetime.datetime.now()-self.get_last_refresh_datetime()).seconds
        if delta>settings.TEEWORLDS_MONITOR_SERVERS_REFRESH_INTERVAL:
            print "Fetching info from masterservers..."
            for serverip, serverport in get_all_servers():
                s = self.filter(ip=serverip, port=serverport)
    
                if len(s) == 0:
                    print u"New server: %s:%d" % (serverip, serverport)
                    newserver = Server(ip=serverip, port=serverport)
                    newserver.refresh()
                elif len(s)==1:
                    s[0].refresh()
                else:
                    raise AssertionError
    
    def get_last_refresh_datetime(self):
        try:
            return self.latest("check_stamp").check_stamp
        except Server.DoesNotExist:
            return datetime.datetime.fromtimestamp(0)
    
    def get_num_online_players(self):
        return sum([server.current_num_players() for server in self.online()])
        
    def online(self):
        return self.filter(online=True)

    def offline(self):
        return self.filter(online=False)

        

class Server(models.Model):
    """
    Teeworlds Server record
    """
    name = models.CharField(max_length=256)
    ip = models.IPAddressField()
    port = models.PositiveIntegerField()
    online = models.BooleanField()
    check_stamp = models.DateTimeField(auto_now=True)
    interested_stamp = models.DateTimeField(null=True)    
    version = models.CharField(max_length=64, null=True)
    max_num_players = models.PositiveIntegerField(null=True)
    progression = models.IntegerField(null=True)
    flags = models.IntegerField(null=True)
    
    objects = ServerManager()
    
    class Meta:
        get_latest_by = "check_stamp"
        
    def refresh(self):
        try:
            delta = (datetime.datetime.now() - self.check_stamp).seconds
        except:
            delta = 0
        try:
            delta_interested = (datetime.datetime.now() - self.interested_stamp).seconds
        except:
            delta_interested = settings.TEEWORLDS_MONITOR_INTERESTED_TIMEOUT
        if self.check_stamp is None\
           or delta>settings.TEEWORLDS_MONITOR_SERVER_REFRESH_INTERVAL \
           or delta_interested<settings.TEEWORLDS_MONITOR_INTERESTED_TIMEOUT:
            res = get_server_info(self.ip, self.port)
            if res is not None:
                self.name = res['name']
                self.max_num_players = res['max_players']
               
                self.current_map = res['map']
                self.flags = res['flags']
                old_progression = self.progression
                self.progression = res['progression']
                self.version = res['version']
                self.online = True

                self.save()
                print u"Server %s:%d (%s) data refreshed" % \
                        (self.ip, self.port, self.name)
                
                if self.progression<old_progression or len(self.match_set.all())==0:
                    self.match_set.create(\
                        gametype = GameType.objects.get_or_create(name = res['gametype'])[0],
                        gametype_name = res['gametype_name'],
                        gamemap = GameMap.objects.get_or_create(name = res['map'])[0],
                    )
                self.match_set.latest().refresh_players(res['players'])
                

                self.nums_players.create(data=res['num_players'])
 
            else:
                self.online = False
                print u"Server %s:%d is offline" % \
                        (self.ip, self.port)
                self.save()
            
    def interested(self):
        self.interested_stamp = datetime.datetime.now()
        self.save()
        
    def current_num_players(self):
        return self.nums_players.latest().data
            
    def __unicode__ (self):
        if self.online:
            online = u"*"
        else:
            online = u"-"
        return u"(%s) %s:%d %s" % (online, self.ip, self.port, self.name)


    
class NumberPlayers(StatisticalData):
    server = models.ForeignKey(Server, related_name="nums_players")

    
class GameType(models.Model):
    name = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.name

    
class GameMap(models.Model):
    name = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.name
    
    
class Player(models.Model):
    name = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.name
    
   
class Match(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    server = models.ForeignKey(Server)
    gametype = models.ForeignKey(GameType)
    gametype_name = models.CharField(max_length=64, null=True)
    gamemap = models.ForeignKey(GameMap)
    players = models.ManyToManyField(Player, null=True)
    
    class Meta:
        get_latest_by = "started"
    
    def refresh_players(self, players):
        for player_dict in players:
            player, created = Player.objects.get_or_create(name=player_dict['name'])
            self.players.add(player)
            self.score_set.create(player=player, data=player_dict['score'])

    def __unicode__(self):
        return u"%s @ %s" % (self.gametype, self.gamemap)
    
class Score(StatisticalData):
    player = models.ForeignKey(Player, related_name="score_set")
    match = models.ForeignKey(Match)
    
    def __unicode__(self):
        return self.data
   