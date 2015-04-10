from django.contrib import admin
from .models import DirectMessage, MessageChain


class DirectMessageAdmin(admin.ModelAdmin):
    
    class Meta:
        model = DirectMessage
        
class MessageChainAdmin(admin.ModelAdmin):
    
    class Meta:
        model = MessageChain
        
admin.site.register(DirectMessage, DirectMessageAdmin)
admin.site.register(MessageChain, MessageChainAdmin)
