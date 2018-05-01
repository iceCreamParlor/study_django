# -*- coding: utf-8 -*- 
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from restaurant.models import RestaurantLocation
# Create your models here.

class Item(models.Model):
    #associations
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant = models.ForeignKey(RestaurantLocation)
    # item stuff
    name = models.CharField(max_length=120)
    contents = models.TextField(help_text = 'separate each item by comma')
    excludes = models.TextField(blank=True, null=True, help_text = 'separate each item by comma')
    public = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('menus:detail', kwargs={'pk':self.pk} ) # you can send parameter slug to urls.py, views.py
    class Meta:
        ordering = ['-updated', '-timestamp'] # updated, timestamp가 늦은 순서대로, -를 빼면 시간 순서대로 정렬된다. 

    def get_contents(self):
        return self.contents.split(",")
    def get_excludes(self):
        return self.excludes.split(",")

class HealthClub(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name

class HealthDiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub = models.ForeignKey(HealthClub)
    timestamp = models.DateTimeField(auto_now=True)

