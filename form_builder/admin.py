from django.contrib import admin
from .models import CLIPManifest, SkipperConfigManifest, Fastq

# make model visible on the admin page
admin.site.register(CLIPManifest)
admin.site.register(Fastq)
admin.site.register(SkipperConfigManifest)
# Register your models here.
