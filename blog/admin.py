from django.contrib import admin
from .models import Post

# make model visible on the admin page
admin.site.register(Post)

# Register your models here.
