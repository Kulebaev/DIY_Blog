from django.contrib import admin
from .models import UserProfile, UserPost, Comment 

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPost)
admin.site.register(Comment)
