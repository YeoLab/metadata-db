from django.contrib import admin
from .models import Post, CLIP, Fastq

# make model visible on the admin page
admin.site.register(Post)
admin.site.register(CLIP)
admin.site.register(Fastq)

# Register your models here.
