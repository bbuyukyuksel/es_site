from django.db import models

# Create your models here.
class Node(models.Model):
    device_name = models.CharField(max_length=200, verbose_name='Device Name', unique=True)
    power_state = models.BooleanField(verbose_name="Power State", default=False)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)

    def __str__(self):
        return self.device_name

class Temperature(models.Model):
    device = models.ForeignKey(Node, on_delete=models.CASCADE)
    temperature = models.FloatField(verbose_name='Temperature')
    created_date = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    
    def __str__(self):
        return 'Temperature: {:10}, Device: {:10}, {}'.format(str(self.temperature), str(self.device), str(self.created_date))
