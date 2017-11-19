# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from composite_pk import composite

import xml.etree.ElementTree
import numpy as np


class Site(models.Model):
    stid = models.CharField(primary_key=True, max_length=255)
    number = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    nearest_city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    distance_from_town = models.FloatField(blank=True, null=True)
    direction_from_town = models.CharField(max_length=3, blank=True, null=True)
    climate_division = models.SmallIntegerField(blank=True, null=True)
    climate_division_name = models.CharField(max_length=255, blank=True, null=True)
    wfo = models.CharField(max_length=3, blank=True, null=True)
    commissioned = models.DateTimeField(blank=True, null=True)
    decommissioned = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sites'


class Lidar(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    stid = models.CharField(max_length=255, blank=True, null=True)
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='site', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lidars'


class Scan(models.Model):
    lidar = models.ForeignKey(Lidar, models.DO_NOTHING)
    id = models.SmallIntegerField(primary_key=True)
    xml = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'scans'

    # a nice function that anyone can use
    def get_ranges(xml_str):
        scan = xml.etree.ElementTree.fromstring(xml_str).find('.//scan')
        if 'display_resolution_m' in scan.attrib.keys():
            range_min = float(scan.attrib['minimum_range_m'])
            range_res = float(scan.attrib['display_resolution_m'])
            ngates = int(scan.attrib['number_of_gates'])
            ranges = range_min + np.arange(ngates) * range_res
        else:
            ranges = np.fromstring(scan.attrib['distances_m'], sep=', ')
        return ranges

    @property
    def ranges(self):
        return self.get_ranges(self.xml)


class Mwr(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    stid = models.CharField(unique=True, max_length=255)
    site = models.ForeignKey('Site', models.DO_NOTHING, db_column='site', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mwrs'

    # just for convenient reference
    mwr_vars = ['temp', 'vapor', 'liquid', 'rh']
    ranges = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
              0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
              1.6, 1.7, 1.8, 1.9, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25,
              3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75,
              6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25,
              8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0]

    # @property
    # def ranges(self):
    #     return [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
    #             0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
    #             1.6, 1.7, 1.8, 1.9, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25,
    #             3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75,
    #             6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25,
    #             8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0]

    
class MwrScan(models.Model):
    mwr = models.ForeignKey(Mwr, models.DO_NOTHING)
    id = models.SmallIntegerField(primary_key=True)
    processor = models.TextField()

    class Meta:
        managed = False
        db_table = 'mwr_scans'


# need a router to make sure these go to the right place
class CommonRouter(object):
    apps = ['common', 'profiles']
    def __init__(self):
        # just want to have the apps associated with the lidar
        # database here so I can control all of them in one place
        self.apps = ['common', 'profiles']
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps:
            return 'lidar'
        return None
    def db_for_write(self, model, **hints):
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.apps or \
           obj2._meta.app_label in self.apps:
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'lidar':
            return False
        return None





# not using these for now:

# class Lidar5M(models.Model):
#     scan = models.ForeignKey('Scans', models.DO_NOTHING, primary_key=True)
#     time = models.DateTimeField()
#     cnr = models.TextField(blank=True, null=True)  # This field type is a guess.
#     drws = models.TextField(blank=True, null=True)  # This field type is a guess.
#     xwind = models.TextField(blank=True, null=True)  # This field type is a guess.
#     ywind = models.TextField(blank=True, null=True)  # This field type is a guess.
#     zwind = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = 'lidar5m'
#         unique_together = (('scan', 'time'),)


# class Lidar30M(models.Model):
#     scan = models.ForeignKey('Scans', models.DO_NOTHING, primary_key=True)
#     time = models.DateTimeField()
#     tke = models.TextField(blank=True, null=True)  # This field type is a guess.
#     alpha = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = 'lidar30m'
#         unique_together = (('scan', 'time'),)


# class Profiles(models.Model):
#     lidar = models.ForeignKey(Lidars, models.DO_NOTHING, primary_key=True)
#     configuration_id = models.SmallIntegerField(blank=True, null=True)
#     scan = models.ForeignKey('Scans', models.DO_NOTHING)
#     sequence_id = models.IntegerField(blank=True, null=True)
#     los_id = models.SmallIntegerField(blank=True, null=True)
#     azimuth = models.FloatField(blank=True, null=True)
#     elevation = models.FloatField(blank=True, null=True)
#     time = models.DateTimeField()
#     cnr = models.TextField(blank=True, null=True)  # This field type is a guess.
#     rws = models.TextField(blank=True, null=True)  # This field type is a guess.
#     drws = models.TextField(blank=True, null=True)  # This field type is a guess.
#     status = models.TextField(blank=True, null=True)  # This field type is a guess.
#     error = models.TextField(blank=True, null=True)  # This field type is a guess.
#     confidence = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = 'profiles'
#         unique_together = (('lidar', 'time'),)


# class Wind(models.Model):
#     lidar = models.ForeignKey(Lidars, models.DO_NOTHING, primary_key=True)
#     scan = models.ForeignKey(Scans, models.DO_NOTHING)
#     time = models.DateTimeField()
#     xwind = models.TextField(blank=True, null=True)  # This field type is a guess.
#     ywind = models.TextField(blank=True, null=True)  # This field type is a guess.
#     zwind = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = 'wind'
#         unique_together = (('lidar', 'time'),)


class MwrProfile(models.Model):
    scan = models.ForeignKey('MwrScan', models.DO_NOTHING, primary_key=True)
    time = models.DateTimeField(primary_key=True)
    mwr = models.ForeignKey('Mwr')
    processor = models.CharField(max_length=255)
    # for the composite primary key
    objects = composite.CompositePKManager()
    
    temp = ArrayField(models.FloatField(blank=True, null=True))
    vapor = ArrayField(models.FloatField(blank=True, null=True))
    liquid = ArrayField(models.FloatField(blank=True, null=True))
    rh = ArrayField(models.FloatField(blank=True, null=True))
    tempq = models.NullBooleanField()
    vaporq = models.NullBooleanField()
    liquidq = models.NullBooleanField()
    rhq = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'mwr_profiles'
        unique_together = (('scan', 'time'),)
        get_latest_by = 'time'
