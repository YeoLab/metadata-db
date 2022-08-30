from django.contrib import admin
from .models import Post, CLIP

# make model visible on the admin page
admin.site.register(Post)
admin.site.register(CLIP)

# Register your models here.
