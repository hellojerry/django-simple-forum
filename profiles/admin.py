from django.contrib import admin
from profiles.models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
        
        
admin.site.register(Profile, ProfileAdmin)
    
