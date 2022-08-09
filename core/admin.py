from django.contrib import admin
from .models import (
    Profile, 
    Post, 
    comment, 
    LikePost,
    FolowerCount,
    )
# Register your models here.

class commentInline(admin.StackedInline):
    model = comment
    extra = 3
class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [commentInline]

admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost)
admin.site.register(FolowerCount)