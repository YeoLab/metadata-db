from django.contrib import admin
from .models import Post, CLIPManifest, Fastq

# make model visible on the admin page
admin.site.register(Post)
admin.site.register(CLIPManifest)
admin.site.register(Fastq)

# Register your models here.
