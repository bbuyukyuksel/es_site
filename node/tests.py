import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "es_site.settings")
import django
django.setup()

#from django.test import TestCase
from node.models import Node, Temperature
from django.utils import timezone
import datetime
import random

# Create your tests here.

'''
# Create Data
node = Node.objects.all()[1]
for i in range(10):
    print("Dayoffset", i)
    for data_size in range(5):
        temp = random.randint(10, 60)
        node.temperature_set.create(temperature=temp)
'''

'''
# Update Date
node = Node.objects.all()[1]
for i in range(10):
    day = timezone.now() - datetime.timedelta(days=i)
    print("+For Day", str(day.date))
    for data_size in range(5):
        print(" index", i*5+data_size)
        temp_object = node.temperature_set.all()[i*5+data_size]
        temp_object.created_date = day
        temp_object.save()
        print(node.temperature_set.all()[i*5+data_size])
'''

 

