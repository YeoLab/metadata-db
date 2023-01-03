# imports
from django.contrib.auth.decorators import login_required
from mysite import settings
from .models import Fastq
from django.shortcuts import render
from .forms import CLIPManifestForm, SkipperConfigManifestForm
from .utils import *

@login_required
def CLIP_form(request):
    fastq = Fastq.objects.filter(submitter=request.user)
    if request.method == 'POST':
        form = CLIPManifestForm(request.POST)
        data = make_CLIP_form(form, request)
        if data:
            return data
    else:
        form = CLIPManifestForm()
    
    return render(request, 'form_builder/CLIP_form.html', {'form': form,
                                                           'fastq': fastq})

@login_required
def SKIPPER_form(request):
    fastq = Fastq.objects.filter(submitter=request.user)
    if request.method == 'POST':
        form = SkipperConfigManifestForm(request.POST)
        data = make_SKIPPER_form(form, request)
        if data:
            return data
    else:
        form = SkipperConfigManifestForm()
    return render(request, 'form_builder/SKIPPER_form.html', {'form': form, 
                                                              'fastq': fastq})

def index_view(request):
    context = {'LOGIN_URL': settings.LOGIN_URL}
    template = 'form_builder/index.html'
    return render(request, template, context)
