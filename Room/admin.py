from django.contrib import admin

# Register your models here.
from .models import UserProfile, Room, Application

admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Application)
