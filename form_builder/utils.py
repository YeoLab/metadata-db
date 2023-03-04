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

        '''
        ip_fastq_path = request.POST.get("ip_fastq_path")
        ip_adapter_path = request.POST.get("ip_adapter_path")
        sminput_fastq_path = request.POST.get("sminput_fastq_path")
        sminput_adapter_path = request.POST.get("sminput_adapter_path")
        ip_rep = request.POST.get("ip_rep")
        sminput_rep = request.POST.get("sminput_rep")
        '''

        make_fastq(ip_fastq_path, ip_adapter_path, ip_rep, sminput_fastq_path,
                   sminput_adapter_path, sminput_rep,
                   cells, experiment, sample, submitter, request)
    else:                               # Delete fastq
        for key in request.POST.keys():
            if key.startswith('delete_fqid_'):
                SingleEndFastq.objects.filter(
                    id=int(key.split('delete_fqid_')[1])).delete()

def make_SKIPPER_form(form, request):
    '''
    If download manifest button is clicked, generates list of FASTQs, 
    and csv file is downloaded onto the page. If download config button is 
    clicked, will download a 'Skipper_config.py file'. If adding sample, 
    creates a new FASTQ object. Otherwise, deletes FASTQ object.
    Args:
        form: SkipperConfigManifestForm
        request: HttpRequest

    Returns:
        response: HttpResponse
    '''
    if request.POST.get("save_manifest"):   # "Save and Download MANIFEST"
        fastqs = []
        for key in request.POST.keys():     # generate list of fastqs
            try:
                if key.startswith('fqid_'): 
                    SingleEndFastq.objects.get(pk=request.POST.get(key))
                    fastqs.append(request.POST.get(key))
            except Exception as e:
                print(e)  
                pass

        if form.is_valid():
            clip = form.save(commit=False)
            clip.fastqs = ','.join(fastqs)
            clip.save()
            file_data = skipper_tsv(clip)   # generate tsv 
            response = HttpResponse(
                file_data, content_type='application/text charset=utf-8')
            f = request.POST.get('manifest', 'manifest.csv')
            response['Content-Disposition'] = f'attachment; filename="{f}"'
            return response

    elif request.POST.get("save_config"):   # "Save and Download CONFIG"
        if form.is_valid():
            clip = form.save(commit=False)
            clip.save()
            file_data = skipper_config(clip)
            response = HttpResponse(
                file_data, content_type='application/text charset=utf-8')
            f = 'Skipper_config.py'
            response['Content-Disposition'] = f'attachment; filename="{f}"'
            return response

    elif request.POST.get("newItem"):       # "Add Sample" button
        ip_fastq_path = request.POST.get("ip_fastq_path", None)
        ip_adapter_path = request.POST.get("ip_adapter_path", None)
        sminput_fastq_path = request.POST.get("sminput_fastq_path", None)
        sminput_adapter_path = request.POST.get("sminput_adapter_path", None)
        cells = request.POST.get("cells", None)
        experiment = request.POST.get("experiment", None)
        sample = request.POST.get("sample", None)
        ip_rep = request.POST.get("ip_rep", None)
        sminput_rep = request.POST.get("sminput_rep", None)
        submitter = request.user

        make_fastq(ip_fastq_path, ip_adapter_path, ip_rep, sminput_fastq_path,
                    sminput_adapter_path, sminput_rep,
                    cells, experiment, sample, submitter, request)
    else:                                   # Delete fastq
        for key in request.POST.keys():
            if key.startswith('delete_fqid_'):
                    SingleEndFastq.objects.filter(
                    id=int(key.split('delete_fqid_')[1])).delete()

def make_fastq(ip_fastq_path, ip_adapter_path, ip_rep, sminput_fastq_path,
               sminput_adapter_path, sminput_rep,
               cells, experiment, sample, submitter, request):
    '''
    Checks for valid FASTQs. Will output a message popup if fields are invalid 
    or incomplete or duplicates exist. For valid FASTQs, will create a FASTQ 
    Object.
    Args:
        ip_fastq_path: string
        ip_adapter_path: string
        ip_rep: string
        sminput_fastq_path: string
        sminput_adapter_path: string
        sminput_rep: string
        cells: string
        experiment: string
        sample: string
        submitter: string
        request: HttpRequest

    Returns:

    '''
    # complete fields
    if ip_fastq_path is None or ip_adapter_path is None or ip_rep is None or \
            sminput_fastq_path is None or sminput_adapter_path is None or \
            sminput_rep is None or cells is None or experiment is None or \
            sample is None or submitter is None:
        messages.error(
            request,
            f'Failed to add sample {sample} to the database \
                (are all fields completed?)'
        )

    # duplicate fastq paths
    elif len(SingleEndFastq.objects.filter(sample=sample, ip_path=ip_fastq_path,
                                  sminput_path=sminput_fastq_path)) > 0:
        messages.error(
            request,
            f'Fastq path: {ip_fastq_path} and {sminput_fastq_path} already \
                exists! Refusing to add to database.'
        )

    # duplicate reps for same sample
    elif len(SingleEndFastq.objects.filter(sample=sample, ip_rep=ip_rep,
                                  sminput_rep=sminput_rep,
                                  submitter=request.user)) > 0:
        messages.error(
            request,
            f'IP Replicate {ip_rep} and Size-matched Input Replicate \
                {sminput_rep} for sample {sample} already exists! Refusing to \
                add to database.'
        )

    # valid fastq
    else:
        # warning for duplicate ip rep
        if len(SingleEndFastq.objects.filter(sample=sample, ip_rep=ip_rep,
                                    submitter=request.user)) > 0:
            messages.warning(
                request,
                f'Warning - {sample} IP Replicate {ip_rep} exists in database \
                    (but with a different Size-matched Input replicate).'
            )
        # warning for duplicate input rep
        if len(SingleEndFastq.objects.filter(sample=sample, sminput_rep=sminput_rep,
                                    submitter=request.user)) > 0:
            messages.warning(
                request,
                f'Warning - {sample} Size-matched Input Replicate \
                    {sminput_rep} exists in database (but with a different \
                    IP replicate).'
            )
        # create fastq object with submitted fields
        SingleEndFastq.objects.create(
            submitter=submitter,
            experiment=experiment,
            sample=sample,
            ip_title=sample + "_CLIP_" + ip_rep,
            ip_rep=ip_rep,
            ip_path=ip_fastq_path,
            ip_adapter_path=ip_adapter_path,
            ip_complete=False,
            cells=cells,
            sminput_title=sample + "_SMINPUT_" + sminput_rep,
            sminput_rep=sminput_rep,
            sminput_path=sminput_fastq_path,
            sminput_adapter_path=sminput_adapter_path,
            sminput_complete=False
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
                    {'name': fastq.ip_title,
                        'read1': {'class': 'File', 'path': fastq.ip_path},
                        'adapters': {'class': 'File',
                                     'path': fastq.ip_adapter_path}},
                    {'name': fastq.sminput_title,
                        'read1': {'class': 'File', 'path': fastq.sminput_path},
                        'adapters': {'class': 'File',
                                     'path': fastq.sminput_adapter_path}},
                ])
        elif field in ['speciesGenomeDir', 'repeatElementGenomeDir']:
            field_dict[field] = {'class': 'Directory', 'path': value}
        elif field in ['chrom_sizes', 'blacklist_file']:
            field_dict[field] = {'class': 'File', 'path': value}
        elif field != '_state' and field != 'barcode_file' and field != 'id':
            field_dict[field] = value
    return "#!/usr/bin/env eCLIP_singleend\n" + yaml.dump(
        field_dict, default_flow_style=False)

def skipper_tsv(clip):
    '''
    Create TSV of SKIPPER form
    Args:
        clip: SkipperConfigManifestForm

    Returns:
        rows: string
    '''
    rows = ','.join([
        'Experiment', 'Sample', 'Cells',
        'Input_replicate', 'Input_adapter', 'Input_fastq',
        'CLIP_replicate', 'CLIP_adapter', 'CLIP_fastq',
        '\n'
    ])

    for field, value in clip.__dict__.items():
        if field == 'fastqs':
            for i in value.split(','):
                fastq = SingleEndFastq.objects.get(pk=i)
                row = ','.join([
                    fastq.experiment,
                    fastq.sample,
                    fastq.cells,
                    str(fastq.ip_rep),
                    fastq.sminput_adapter_path,
                    fastq.sminput_path,
                    str(fastq.sminput_rep),
                    fastq.ip_adapter_path,
                    fastq.ip_path,
                ])
                rows += row + "\n"
    return rows

def skipper_config(clip):
    '''
    Create CONFIG from SKIPper form
    Args:
        clip: SkipperConfigManifestForm

    Returns:
        config_string: string
    '''
    config_string = ""
    for field, value in clip.__dict__.items():
        if field == 'informative_read' or field == 'uninformative_read' or \
                field == 'umi_size':
            config_string += f'{field.upper()} = {value}\n'
        elif field != '_state' and field != 'id' and \
                field != 'barcode_file' and field != 'fastqs':
            config_string += f'{field.upper()} = \"{value}\"\n'
    return config_string
