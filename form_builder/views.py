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
    files = []
    try:
        SEfastqs = SingleEndFastq.objects.filter(submitter=request.user)
    except Exception as e:
        print(e)
        SEfastqs = []

    if request.method == 'POST':
        form = CLIPManifestForm(request.POST)
        data = make_CLIP_form(form, request)
        if data:
            return data
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
        'globus_url': "https://app.globus.org/file-manager?method=GET&origin_id=d9358457-3f23-4b35-bbae-68d2f4190545&origin_path=%2F&action=http://localhost:8000/clipper/"
    }
    return render(request, 'form_builder/CLIP_form.html', context=context)

'''
@login_required
def SKIPPER_form(request):
    fastq = SingleEndFastq.objects.filter(submitter=request.user)
    if request.method == 'POST':
        form = SkipperConfigManifestForm(request.POST)
        data = make_SKIPPER_form(form, request)
        if data:
            return data
    else:
        form = SkipperConfigManifestForm()
    return render(request, 'form_builder/SKIPPER_form.html', {'form': form}) #, 'fastq': fastq})


def rnaseqSE_form(request):
    fastq = SingleEndFastq.objects.filter(submitter=request.user)
    # submit form with filled out fields
    if request.method == 'POST':
        form = RnaseqForm(request.POST)
        # downloading yaml file
        if request.POST.get("save"):
            fastqs = []
            for key in request.POST.keys():
                try:
                    # find added fastqs
                    if key.startswith('fqid_'):
                        Fastq.objects.get(pk=request.POST.get(key))
                        # append to fastq array
                        fastqs.append(request.POST.get(key))
                except Exception as e:
                    print(e)
                    pass

            # filled out form fields
            if form.is_valid():
                rnaseq = form.save(commit=False)
                rnaseq.fastqs = ','.join(fastqs)
                rnaseq.save()
                # generate yaml file
                file_data = rnaseqSE_yaml(rnaseq)
                response = HttpResponse(
                    file_data, content_type='application/text charset=utf-8')
                f = request.POST.get('dataset', 'manifest')
                # download attachment
                response['Content-Disposition'] = f'attachment; filename="{f}.yaml"'
                return response
    # blank form
    else:
        form = RnaseqForm()
    return render(request, 'form_builder/rnaseqSE_form.html', {'form': form})


def rnaseqPE_form(request):
    fastq = SingleEndFastq.objects.filter(submitter=request.user)
    # submit form with filled out fields
    if request.method == 'POST':
        form = RnaseqForm(request.POST)
        # downloading yaml file
        if request.POST.get("save"):
            fastqs = []
            for key in request.POST.keys():
                try:
                    # find added fastqs
                    if key.startswith('fqid_'):
                        Fastq.objects.get(pk=request.POST.get(key))
                        # append to fastq array
                        fastqs.append(request.POST.get(key))
                except Exception as e:
                    print(e)
                    pass

            # filled out form fields
            if form.is_valid():
                rnaseq = form.save(commit=False)
                rnaseq.fastqs = ','.join(fastqs)
                rnaseq.save()
                # generate yaml file
                file_data = rnaseqPE_yaml(rnaseq)
                response = HttpResponse(
                    file_data, content_type='application/text charset=utf-8')
                f = request.POST.get('dataset', 'manifest')
                # download attachment
                response['Content-Disposition'] = f'attachment; filename="{f}.yaml"'
                return response
    # blank form
    else:
        form = RnaseqForm()
    return render(request, 'form_builder/rnaseqPE_form.html', {'form': form})


def rnaseqSE_yaml(rnaseq):
    field_dict = dict()
    field_dict['reads'] = []
    for field, value in rnaseq.__dict__.items():
        if field == 'fastqs':
            for i in value.split(','):
                fastq = Fastq.objects.get(pk=i)
                field_dict['reads'].append([
                    # TODO: replace empty strings with necessary components
                    {'name':  fastq.ip_title + '-rep' + '',
                     'read1': {'class': 'File', 'path': ''}},
                ])
        elif field in ['speciesGenomeDir', 'repeatElementGenomeDir']:
            field_dict[field] = {'class': 'Directory', 'path': value}
        elif field in ['speciesChromSizes', 'b_adapters']:
            field_dict[field] = {'class': 'File', 'path': value}
        elif field != '_state' and field != 'barcode_file' and field != 'id':
            field_dict[field] = value
    return "#!/usr/bin/env RNASEQ_singleend\n" + yaml.dump(field_dict, default_flow_style=False)

def rnaseqPE_yaml(rnaseq):
    pass
'''

def index_view(request):
    context = {'LOGIN_URL': settings.LOGIN_URL}
    template = 'form_builder/index.html'
    return render(request, template, context)


@csrf_exempt
def receive_data(request):
    print('post', request.POST)

    context = {}
    return render(request, 'form_builder/receive-data.html', context)