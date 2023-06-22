# imports
from django.contrib import messages
from .models import SingleEndFastq
import yaml
from django.http import HttpResponse

def make_CLIP_form(form, request):
    '''
    If download CLIPPER button is clicked, generates list of FASTQs, 
    and yaml file is downloaded onto the page. If adding sample, creates a new 
    FASTQ object. Otherwise, deletes FASTQ object.
    Args:
        form: CLIPManifestForm
        request: HttpRequest

    Returns:
        response: HttpResponse
    '''
    if request.POST.get("save"):        # "Save and Download (CLIPper)" button
        fastqs = []
        for key in request.POST.keys():  # generate list of fastqs
            try:
                if key.startswith('fqid_'):
                    SingleEndFastq.objects.get(pk=request.POST.get(key))
                    fastqs.append(request.POST.get(key))
            except Exception as e:
                print(e)
                pass

        if form.is_valid():             # save valid form and download YAML
            clip = form.save(commit=False)
            clip.fastqs = ','.join(fastqs)
            clip.save()

            file_data = CLIP_yaml(clip)
            response = HttpResponse(
                file_data, content_type='application/text charset=utf-8')
            f = request.POST.get('dataset', 'manifest')
            response['Content-Disposition'] = f'attachment; filename="{f}.yaml"'
            return response

    elif request.POST.get("newItem"):   # "Add Sample" button
        experiment = request.POST.get("experiment")
        sample = request.POST.get("sample")
        cells = request.POST.get("cells")
        replicate = request.POST.get("replicate")
        path = request.POST.get("path")
        adapter = request.POST.get("adapter")
        submitter = request.user

        make_fastq(replicate, path, adapter, cells, experiment, sample, 
                   submitter, request)
        
    else:                               # Delete fastq
        for key in request.POST.keys():
            if key.startswith('delete_fqid_'):
                SingleEndFastq.objects.filter(
                    id=int(key.split('delete_fqid_')[1])).delete()


def make_fastq(replicate, path, adapter, cells, experiment, sample, 
                   submitter, request): 
    '''
    Checks for valid FASTQs. Will output a message popup if fields are invalid 
    or incomplete or duplicates exist. For valid FASTQs, will create a FASTQ 
    Object.
    Args:
        replicate: string
        path: string
        adapter: string
        cells: string
        experiment: string
        sample: string
        submitter: string
        request: HttpRequest

    Returns:

    '''
    # complete fields
    if path is None or replicate is None or adapter is None or \
        cells is None or experiment is None or sample is None or \
        submitter is None:
        messages.error(
            request,
            f'Failed to add sample {sample} to the database \
                (are all fields completed?)'
        )

    # duplicate fastq paths
    elif len(SingleEndFastq.objects.filter(sample=sample, path=path)) > 0:
        messages.error(
            request,
            f'Fastq path: {path} already exists! Refusing to add to database.'
        )

    # duplicate reps for same sample
    elif len(SingleEndFastq.objects.filter(sample=sample, replicate=replicate,
                                  submitter=request.user)) > 0:
        messages.error(
            request,
            f'Replicate {replicate} for sample {sample} already exists! \
                Refusing to add to database.'
        )

    # valid fastq
    else:
        # create fastq object with submitted fields
        SingleEndFastq.objects.create(
            submitter=submitter,
            experiment=experiment,
            sample=sample,
            title=sample + "_CLIP_" + replicate,
            replicate=replicate,
            path=path,
            cells=cells,
            adapter_path=adapter,
        )
    return

def CLIP_yaml(clip):
    '''
    Create a dictionary to generate YAML from CLIP form
    Args:
        clip: CLIPManifestForm

    Returns:
        string
    '''
    field_dict = dict()
    field_dict['samples'] = []

    for field, value in clip.__dict__.items():
        if field == 'fastqs':
            for i in value.split(','):
                fastq = SingleEndFastq.objects.get(pk=i)
                field_dict['samples'].append([
                    {'name': fastq.title,
                        'read1': {'class': 'File', 'path': fastq.path},
                        'adapters': {'class': 'File',
                                     'path': fastq.adapter_path}},
                    {'name': fastq.title,
                        'read1': {'class': 'File', 'path': fastq.path},
                        'adapters': {'class': 'File',
                                     'path': fastq.adapter_path}},
                ])
        elif field in ['speciesGenomeDir', 'repeatElementGenomeDir']:
            field_dict[field] = {'class': 'Directory', 'path': value}
        elif field in ['chrom_sizes', 'blacklist_file']:
            field_dict[field] = {'class': 'File', 'path': value}
        elif field != '_state' and field != 'barcode_file' and field != 'id':
            field_dict[field] = value
    return "#!/usr/bin/env eCLIP_singleend\n" + yaml.dump(
        field_dict, default_flow_style=False)