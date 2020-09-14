from django.contrib import admin
from .models import User, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "timestamp", "likes")
# Register your models here.

admin.site.register(User)
admin.site.register(Post, PostAdmin)
