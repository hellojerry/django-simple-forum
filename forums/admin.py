from django.contrib import admin

from .models import Forum, Thread, Post, ForumCategory

# Register your models here.

class ForumCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = ForumCategory


class ForumAdmin(admin.ModelAdmin):
    class Meta:
        model = Forum

class ThreadAdmin(admin.ModelAdmin):
    class Meta:
        model = Thread
        
class PostAdmin(admin.ModelAdmin):
    class Meta:
        model = Post
        fields = ['__unicode__', 'id', 'author', 'thread', 'created', 'edited']


admin.site.register(ForumCategory, ForumCategoryAdmin)        
admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread,ThreadAdmin)
admin.site.register(Post,PostAdmin)