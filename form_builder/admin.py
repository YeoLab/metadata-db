from django.contrib import admin
from .models import ClipperManifest, SingleEndFastq #SkipperManifest

# make model visible on the admin page
admin.site.register(ClipperManifest)
#admin.site.register(SkipperManifest)
# Register your models here.
