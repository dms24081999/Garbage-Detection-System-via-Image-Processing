from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from .validators import validate_photo_extension


# Create your models here.


class GarbageDataModel(models.Model):
    photo = models.FileField(upload_to='images/garbage/',blank=False,validators=[validate_photo_extension])
    latitude=models.FloatField(null=True, blank=True, default=None)
    longitude=models.FloatField(null=True, blank=True, default=None)
    formatted_address=models.CharField(max_length=500, blank=True,null=True)
 
    def save(self, *args, **kwargs):
        import requests
        URL = "http://apis.mapmyindia.com/advancedmaps/v1/sqgqtzwc2477fmaxq81kws342q5ek6mo/rev_geocode?lat="+str(self.latitude)+"&lng="+str(self.longitude)
        req = requests.get(url = URL)
        data = req.json()
        # print(data['results'][0]['formatted_address'])
        self.formatted_address = data['results'][0]['formatted_address']
        print(self.formatted_address)
        super(GarbageDataModel, self).save(*args, **kwargs)
        # from django.conf import settings
        # from garbage_object_detection_tensorflow.object_detection import object_detection_runner
        # print("path ",str(self.photo.path))
        # data=object_detection_runner.run(str(self.photo.path))
        # print("Hel"+str(data))