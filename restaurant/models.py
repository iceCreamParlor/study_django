from django.conf import settings # Using User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from .utils import unique_slug_generator
from .validators import validate_category
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL
# Create your models here.
class RestaurantLocationQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip() # 공백 없애기
            return self.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(category__icontains=query)|
                Q(category__iexact=query)|
                Q(location__iexact=query)|
                Q(item__contents__icontains=query)
            ).distinct()
        return self

class RestaurantLocationManager(models.Manager):
    def get_queryset(self):
        return RestaurantLocationQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class RestaurantLocation(models.Model):
    owner  = models.ForeignKey(User) # django models unleashed # class_instance.model_set.all()
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, null=True, blank= True)
    category = models.CharField(max_length=120, null=True, blank=False, validators = [validate_category])
    timestamp = models.DateTimeField(auto_now_add=True)
    #my_date_field = models.DateField(auto_now=False, auto_now_add=False)
    slug = models.SlugField(blank=True, null=True)

    objects = RestaurantLocationManager() # add Model.objects.all

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name # obj.title
    def get_absolute_url(self):
        return reverse('restaurent:detail', kwargs={'slug':slug} ) # you can send parameter slug to urls.py, views.py

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving...')
    print(instance.timestamp)
    if not instance.name:
        instance.name = "Another Name"
    #if not instance.slug:
    #    instance.slug = unique_slug_generator(instance)
    instance.category = instance.category.capitalize()

def rl_post_save_receiver(sender, instance, *args, **kwargs):
    print('saved...')
    print(instance.timestamp)

pre_save.connect(rl_pre_save_receiver, sender = RestaurantLocation)
post_save.connect(rl_post_save_receiver, sender = RestaurantLocation)
