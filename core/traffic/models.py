# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

class Cameras(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("name")
    )
    
    class Meta:
        verbose_name = _("Traffic logs")
        verbose_name_plural = _("Traffic logs")    
    
class Types(models.IntegerChoices):
    heavy_car = 1, _("heavy car")
    car = 2, _("car")
    motorcycle = 3, _("motorcycle")
    heavy_engine= 4, _("heavy engine")
    
class TrafficLogs(models.Model):
    plate_number = models.CharField(
        max_length=6,
        verbose_name=_("plate number"),
    )
    camera_id = models.ForeignKey(
        Cameras,
        on_delete=models.PROTECT,
        verbose_name=_("camera id")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("timestamp")
    )
    type_id = models.IntegerField(
        choices=Types.choices,
        verbose_name=_("type id")
    )
    
    class Meta:
        verbose_name = _("Traffic logs")
        verbose_name_plural = _("Traffic logs")
        indexes = [
            models.Index(fields=['plate_number', 'type_id'], name='plate_type_idx'),            
            models.Index(fields=['camera_id', 'timestamp'], name='camera_time_idx'),
            models.Index(fields=['-timestamp'], name='timestamp_desc_idx'),
        ]