from django.contrib import admin
from .models import User, Post, Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "timestamp", "likes")
# Register your models here.

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
