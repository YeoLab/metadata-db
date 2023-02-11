from django.contrib import admin
from .models import ClipperSingleEndFastq, SkipperSingleEndFastq, Fastq, SkipperSingleEndFastq

# make model visible on the admin page
admin.site.register(ClipperSingleEndFastq)
admin.site.register(SkipperSingleEndFastq)
# Register your models here.
