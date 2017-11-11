from django.db import models
from django.contrib.postgres.fields import ArrayField
from composite_pk import composite
# from collections import OrderedDict

# the 5-minute aggregated lidar data
class Lidar5m(composite.CompositePKModel):
    scan = models.ForeignKey('common.Scan', models.DO_NOTHING, primary_key=True)
    time = models.DateTimeField(primary_key=True)
    # for the composite primary key
    objects = composite.CompositePKManager()
    
    cnr = ArrayField(models.FloatField(blank=True, null=True))
    drws = ArrayField(models.FloatField(blank=True, null=True))
    xwind = ArrayField(models.FloatField(blank=True, null=True))
    ywind = ArrayField(models.FloatField(blank=True, null=True))
    zwind = ArrayField(models.FloatField(blank=True, null=True))

    class Meta:
        managed = False
        db_table = 'lidar5m'
        unique_together = (('scan', 'time'),)
        get_latest_by = 'time'
