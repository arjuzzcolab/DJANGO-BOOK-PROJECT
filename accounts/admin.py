from django.contrib import admin
from .models import userProfiles,loginTable

# Register your models here.
admin.site.register(userProfiles)
admin.site.register(loginTable)