from django.db import models
from django.utils import timezone
from django.db.models import Q
import datetime
import functools
import math

# Create your models here.
class Node(models.Model):
    device_name = models.CharField(max_length=200, verbose_name='Device Name', unique=True)
    power_state = models.BooleanField(verbose_name="Power State", default=False)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)

    def __str__(self):
        return self.device_name

    def temperature_this_mount(self):
        this = timezone.now()
        return self.temperature_set.filter(Q(created_date__year = this.year) and Q(created_date__month = this.month))
    
    def temperature_this_mount_list(self):
        return [x.temperature for x in self.temperature_this_mount()]
        
    def temperature_this_mount_average(self):
        if self.temperature_this_mount().count() > 0:
            if self.temperature_this_mount().count() > 1:
                # Get Average of temperature_this_mount:list
                _sum_ = sum([x.temperature for x in self.temperature_this_mount() ])

                return round(_sum_ / self.temperature_this_mount().count(), 2)
            else:
                return self.temperature_this_mount().first().temperature
        else:
            return None

    def temperature_this_mount_count(self):
        return self.temperature_this_mount().count()

    def temperature_last_update_date(self):
        if self.temperature_set.all().count() > 0:
            print("This Timezone", str(timezone.now()))
            return self.temperature_set.all().order_by('-created_date').first().created_date
        return None

class Temperature(models.Model):
    device = models.ForeignKey(Node, on_delete=models.CASCADE)
    temperature = models.FloatField(verbose_name='Temperature')
    created_date = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    
    def __str__(self):
        return 'Temperature: {:10}, Device: {:10}, {}'.format(str(self.temperature), str(self.device), str(self.created_date))
