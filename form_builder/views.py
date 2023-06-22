# imports
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from mysite import settings
from .models import SingleEndFastq
from django.shortcuts import render
from .forms import CLIPManifestForm#, SkipperConfigManifestForm
from .utils import *
from django.views.decorators.csrf import csrf_exempt
import yaml
from django.http import HttpResponse
import os

@csrf_exempt
@login_required
def CLIP_form(request):
    '''
    Generates the view for the eCLIP form builder.
    Args:
        request: HttpRequest
    Returns:
        HttpResponse
    '''
    # generate list of selected files and existing SEfastqs 
    files = []
    try:
        SEfastqs = SingleEndFastq.objects.filter(submitter=request.user)
        for key in request.GET.keys():
                if key.startswith('file'):
                    files.append(os.path.join(base_url, request.GET.get(key)))
    # error handling
    except Exception as e:
        print(e)
        SEfastqs = []
    # form submission
    if request.method == 'POST':
        form = CLIPManifestForm(request.POST)
        data = make_CLIP_form(form, request)
        if data:
            return data
    # get globus file manager url
    else:
        if request.GET.get('endpoint'):
            base_url = '/projects/ps-yeolab5/seqdata' + request.GET.get('path')
            for key in request.GET.keys():
                if key.startswith('file'):
                    files.append(os.path.join(base_url, request.GET.get(key)))
        form = CLIPManifestForm()

    context = {
        'form': form,
        'SEfastqs': SEfastqs,
        'files': files,
        'globus_url': 
        "https://app.globus.org/file-manager?method=GET&origin_id=d9358457-3f23-4b35-bbae-68d2f4190545&origin_path=%2F&action="+ settings.DOMAIN
    }
    return render(request, 'form_builder/CLIP_form.html', context=context)


def index_view(request):
    '''
    Globus authenticator.
    Args:
        request: HttpRequest
    Return:
        HttpResponse
    '''
    context = {'LOGIN_URL': settings.LOGIN_URL}
    template = 'form_builder/index.html'
    return render(request, template, context)


@csrf_exempt
def receive_data(request):
    '''
    Print POST data.
    Args:
        request: HttpRequest
    Return:
        HttpResponse
    '''
    print('post', request.POST)
    context = {}
    return render(request, 'form_builder/receive-data.html', context)