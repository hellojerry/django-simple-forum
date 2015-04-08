from django.contrib import admin
from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
        
        
admin.site.register(Profile, ProfileAdmin)
    
