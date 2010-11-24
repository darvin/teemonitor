from django.db import models
from django.db.models import Sum, Avg

class StatisticalDataManager(models.Manager):
    use_for_related_fields = True
    def create(self, *args, **kwargs):
        try:
            last = self.latest()
        except:
            last = None
        if last is None or last.data!=kwargs['data']:
            return super(StatisticalDataManager, self).create(*args, **kwargs) 
        else:
            return last
    
    def day(self):
        pass
    
    def hour(self):
        pass

    def month(self):
        pass
        return self.get_query_set().filter(sex='F')
    
    def average(self):
        return self.aggregate(Avg("data"))
    
    def sum(self):
        return self.aggregate(Sum("data"))

class StatisticalData(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    data = models.IntegerField()
    
    objects = StatisticalDataManager()
    
    class Meta:
        get_latest_by = "datetime"
        abstract = True
