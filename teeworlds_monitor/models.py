from django.db import models
from teemonitor.libs.tw_api import get_server_info, get_all_servers
import datetime
########################################################################
SERVER_REFRESH_INTERVAL=60

class ServerManager(models.Manager):
    def refresh(self):
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
            

class Server(models.Model):
    """
    Teeworlds Server record
    """
    
    name = models.CharField(max_length=256)
    ip = models.IPAddressField()
    port = models.PositiveIntegerField()
    online = models.BooleanField()
    check_stamp = models.DateTimeField(auto_now=True)
    
    gametype = models.CharField(max_length=64, null=True)
    gametype_name = models.CharField(max_length=64, null=True)
    version = models.CharField(max_length=64, null=True)
    current_map = models.CharField(max_length=64,null=True )
    current_num_players = models.PositiveIntegerField(null=True)
    max_num_players = models.PositiveIntegerField(null=True)
    progression = models.IntegerField(null=True)
    flags = models.IntegerField(null=True)

    
    objects = ServerManager()
        
    def refresh(self):
        try:
            delta = datetime.datetime.now() - self.check_stamp
        except:
            pass
        if self.check_stamp is None or delta.seconds>SERVER_REFRESH_INTERVAL:
            res = get_server_info(self.ip, self.port)
            if res is not None:
                self.name = res['name']
                self.gametype = res['gametype']
                self.gametype_name = res['gametype_name']
                self.max_num_players = res['max_players']
                self.current_num_players = res['num_players']
                self.current_map = res['map']
                self.flags = res['flags']
                self.progression = res['progression']
                self.version = res['version']
                self.online = True

                print u"Server %s:%d (%s) data refreshed" % \
                        (self.ip, self.port, self.name)
            else:
                self.online = False
                print u"Server %s:%d is offline" % \
                        (self.ip, self.port)
        
            self.save()
    def __unicode__ (self):
        if self.online:
            online = u"*"
        else:
            online = u"-"
        return u"(%s) %s:%d %s" % (online, self.ip, self.port, self.name)
