from django.contrib import admin
from .models import Item, HealthClub, HealthDiary

# Register your models here.
admin.site.register(Item)
admin.site.register(HealthClub)
admin.site.register(HealthDiary)