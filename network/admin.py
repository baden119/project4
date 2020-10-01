from django.contrib import admin
from .models import User, Post, Follow, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "timestamp")
# Register your models here.

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
admin.site.register(Like)
