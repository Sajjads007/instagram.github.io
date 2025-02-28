from django.contrib import admin
from posts.models import UserProfile, Comments, Post, UserAccount

admin.site.register(Comments)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(UserAccount)