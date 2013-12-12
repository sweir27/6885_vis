# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class DateTime(models.Model):
    id = models.IntegerField(primary_key=True)
    t_date = models.DateField(blank=True, null=True)
    t_time = models.TimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'date_time'

class Ip2LocationDb9(models.Model):
    ip_from = models.IntegerField(blank=True, null=True)
    ip_to = models.IntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True)
    country_name = models.CharField(max_length=64, blank=True)
    region_name = models.CharField(max_length=128, blank=True)
    city_name = models.CharField(max_length=128, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    zip_code = models.CharField(max_length=30, blank=True)
    class Meta:
        managed = False
        db_table = 'ip2location_db9'

class NewTable(models.Model):
    id = models.IntegerField(primary_key=True)
    cola = models.CharField(db_column='colA', max_length=45, blank=True) # Field name made lowercase.
    colb = models.CharField(db_column='colB', max_length=45, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'new_table'

class Torrent(models.Model):
    id = models.IntegerField(primary_key=True)
    t_website = models.CharField(max_length=45, blank=True)
    t_category = models.CharField(max_length=20, blank=True)
    t_title = models.CharField(max_length=150, blank=True)
    t_url = models.CharField(max_length=200, blank=True)
    t_sizetype = models.CharField(db_column='t_sizeType', max_length=5, blank=True) # Field name made lowercase.
    t_torrent = models.TextField(blank=True)
    t_size = models.CharField(max_length=10, blank=True)
    class Meta:
        managed = False
        db_table = 'torrent'

class TorrentDatetime(models.Model):
    id = models.IntegerField(primary_key=True)
    torrent = models.ForeignKey(Torrent)
    datetime = models.ForeignKey(DateTime)
    age = models.CharField(max_length=30, blank=True)
    leechers = models.CharField(max_length=10, blank=True)
    seeders = models.CharField(max_length=10, blank=True)
    class Meta:
        managed = False
        db_table = 'torrent_datetime'

class TorrentLocation(models.Model):
    torrent_id = models.IntegerField()
    ip = models.IntegerField()
    country_code = models.CharField(max_length=2, blank=True)
    country_name = models.CharField(max_length=64, blank=True)
    region_name = models.CharField(max_length=128, blank=True)
    city_name = models.CharField(max_length=128, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    zip_code = models.CharField(max_length=30, blank=True)
    ipv4 = models.CharField(max_length=16, blank=True)
    id = models.BigIntegerField(primary_key=True)
    datetime = models.ForeignKey(DateTime)
    class Meta:
        managed = False
        db_table = 'torrent_location'

class Torrents(models.Model):
    id = models.IntegerField(db_column='Id', unique=True) # Field name made lowercase.
    t_website = models.CharField(max_length=45, blank=True)
    t_category = models.CharField(max_length=20, blank=True)
    t_title = models.TextField(blank=True)
    t_url = models.TextField(blank=True)
    t_age = models.CharField(max_length=30, blank=True)
    t_seed = models.CharField(max_length=10, blank=True)
    t_sizetype = models.CharField(db_column='t_sizeType', max_length=5, blank=True) # Field name made lowercase.
    t_torrent = models.TextField(blank=True)
    t_leech = models.CharField(max_length=10, blank=True)
    t_size = models.CharField(max_length=10, blank=True)
    t_date = models.DateField(blank=True, null=True)
    t_time = models.TimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'torrents'

