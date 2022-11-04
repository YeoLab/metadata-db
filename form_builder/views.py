from django.contrib.auth.decorators import login_required
# include model we've written in models.py
# . before models means curr directory or current app
from django.contrib import messages
from mysite import settings
from .models import Fastq
from django.shortcuts import render, redirect
from .forms import CLIPManifestForm, SkipperConfigManifestForm, RnaseqFastqForm
import yaml
from django.http import HttpResponse


@login_required
def CLIP_form(request):
    fastq = Fastq.objects.filter(submitter=request.user)
    # submitting filled out form
    if request.method == 'POST':
        form = CLIPManifestForm(request.POST)
        # downloading yaml file
        if request.POST.get("save"):
            fastqs = []
            for key in request.POST.keys():
                try:
                    # find added fastqs
                    if key.startswith('fqid_'):  # TODO: refactor, hacky
                        Fastq.objects.get(pk=request.POST.get(key))
                        # append to fastq array
                        fastqs.append(request.POST.get(key))
                except Exception as e:
                    print(e)  # TODO: log
                    pass
            
            # filled out form fields
            if form.is_valid():
                clip = form.save(commit=False)
                clip.fastqs = ','.join(fastqs)  # fastqs is a CharField, save all fastq ids as str(comma-separated list)
                clip.save()
                # generate yaml file
                file_data = CLIP_yaml(clip)
                response = HttpResponse(file_data, content_type='application/text charset=utf-8')
                f = request.POST.get('dataset', 'manifest')
                # download attachment
                response['Content-Disposition'] = f'attachment; filename="{f}.yaml"'
                return response

        # adding new fastq
        elif request.POST.get("newItem"):
            # set variables to html form values
            ip_fastq_path = request.POST.get("ip_fastq_path")
            ip_adapter_path = request.POST.get("ip_adapter_path")
            sminput_fastq_path = request.POST.get("sminput_fastq_path")
            sminput_adapter_path = request.POST.get("sminput_adapter_path")
            cells = request.POST.get("cells")
            experiment = request.POST.get("experiment")
            sample = request.POST.get("sample")
            ip_rep = request.POST.get("ip_rep")
            sminput_rep = request.POST.get("sminput_rep")
            submitter = request.user

            # test for valid inputs
            if ip_fastq_path is None or ip_adapter_path is None or ip_rep is None or \
                sminput_fastq_path is None or sminput_adapter_path is None or sminput_rep is None or \
                cells is None or experiment is None or sample is None or submitter is None:
                messages.error(
                    request,
                    f'Failed to add sample {sample} to the database (are all fields completed?)'
                )

            # test for duplicate fastq paths
            elif len(Fastq.objects.filter(sample=sample, ip_path=ip_fastq_path, sminput_path=sminput_fastq_path)) > 0:
                messages.error(
                    request,
                    f' Fastq path: {ip_fastq_path} and {sminput_fastq_path} already exists! Refusing to add to database.'
                )

            # test for duplicate reps for same sample
            elif len(Fastq.objects.filter(sample=sample, ip_rep=ip_rep, sminput_rep=sminput_rep, submitter=request.user)) > 0:
                messages.error(
                    request,
                    f'IP Replicate {ip_rep} and Size-matched Input Replicate {sminput_rep} for \
                    sample {sample} already exists! Refusing to add to database.'
                )

            else:
                if len(Fastq.objects.filter(sample=sample, ip_rep=ip_rep, submitter=request.user)) > 0:
                    messages.warning(
                        request,
                        f'Warning - {sample} IP Replicate {ip_rep} exists in database (but with a different Size-matched Input replicate).'
                    )
                if len(Fastq.objects.filter(sample=sample, sminput_rep=sminput_rep, submitter=request.user)) > 0:
                    messages.warning(
                        request,
                        f'Warning - {sample} Size-matched Input Replicate {sminput_rep} exists in database (but with a different IP replicate).'
                    )
                Fastq.objects.create(
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
        # deleting fastq
        else:
            for key in request.POST.keys():
                if key.startswith('delete_fqid_'):
                    Fastq.objects.filter(id=int(key.split('delete_fqid_')[1])).delete()
    # blank form
    else:
        form = CLIPManifestForm()
    return render(request, 'form_builder/CLIP_form.html', {'form': form, 'fastq': fastq})

@login_required
def SKIPPER_form(request):
    fastq = Fastq.objects.filter(submitter=request.user)

    if request.method == 'POST':
        form = SkipperConfigManifestForm(request.POST)
        if request.POST.get("save_manifest"):
            fastqs = []
            for key in request.POST.keys():
                try:
                    if key.startswith('fqid_'):  # TODO: refactor, hacky
                        Fastq.objects.get(pk=request.POST.get(key))
                        fastqs.append(request.POST.get(key))
                except Exception as e:
                    print(e)  # TODO: log
                    pass

            if form.is_valid():
                clip = form.save(commit=False)
                clip.fastqs = ','.join(fastqs)  # fastqs is a CharField, save all fastq ids as str(comma-separated list)

                clip.save()
                file_data = skipper_tsv(clip)
                response = HttpResponse(file_data, content_type='application/text charset=utf-8')
                f = request.POST.get('manifest', 'manifest.csv')
                response['Content-Disposition'] = f'attachment; filename="{f}"'
                return response
        elif request.POST.get("save_config"):

            if form.is_valid():
                clip = form.save(commit=False)
                clip.save()
                file_data = skipper_config(clip)
                response = HttpResponse(file_data, content_type='application/text charset=utf-8')
                f = 'Skipper_config.py'
                response['Content-Disposition'] = f'attachment; filename="{f}"'
                return response
        elif request.POST.get("newItem"):
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

            if len(Fastq.objects.filter(sample=sample, ip_path=ip_fastq_path, sminput_path=sminput_fastq_path)) > 0:
                messages.error(
                    request,
                    f' Fastq path: {ip_fastq_path} and {sminput_fastq_path} already exists! Refusing to add to database.'
                )
            if ip_fastq_path is None or ip_adapter_path is None or ip_rep is None or \
                sminput_fastq_path is None or sminput_adapter_path is None or sminput_rep is None or \
                cells is None or experiment is None or sample is None or submitter is None:
                messages.error(
                    request,
                    f'Failed to add sample {sample} to the database (are all fields completed?)'
                )
            elif len(Fastq.objects.filter(sample=sample, ip_rep=ip_rep, sminput_rep=sminput_rep, submitter=request.user)) > 0:
                messages.error(
                    request,
                    f'IP Replicate {ip_rep} and Size-matched Input Replicate {sminput_rep} for \
                    sample {sample} already exists! Refusing to add to database.'
                )
            else:
                if len(Fastq.objects.filter(sample=sample, ip_rep=ip_rep, submitter=request.user)) > 0:
                    messages.warning(
                        request,
                        f'Warning - {sample} IP Replicate {ip_rep} exists in database (but with a different Size-matched Input replicate).'
                    )
                if len(Fastq.objects.filter(sample=sample, sminput_rep=sminput_rep, submitter=request.user)) > 0:
                    messages.warning(
                        request,
                        f'Warning - {sample} Size-matched Input Replicate {sminput_rep} exists in database (but with a different IP replicate).'
                    )
                Fastq.objects.create(
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
        else:
            for key in request.POST.keys():
                if key.startswith('delete_fqid_'):
                    Fastq.objects.filter(id=int(key.split('delete_fqid_')[1])).delete()
    else:
        form = SkipperConfigManifestForm()
    return render(request, 'form_builder/SKIPPER_form.html', {'form': form, 'fastq': fastq})

def rnaseq_form(request):
    fastq = Fastq.objects.filter(submitter=request.user)
    # submit form with filled out fields
    if request.method == 'POST':
        form = RnaseqFastqForm(request.POST)
        if form.is_valid():
            rnaseq = form.save(commit=False)
            rnaseq.save()
            # generate yaml file
            file_data = rnaseq_yaml(rnaseq)
            response = HttpResponse(file_data, content_type='application/text charset=utf-8')
            f = request.POST.get('dataset', 'manifest')
            # download attachment
            response['Content-Disposition'] = f'attachment; filename="{f}.yaml"'
            return response
    # blank form
    else:
        form = RnaseqFastqForm()
    return render(request, 'form_builder/rnaseq_form.html', {'form': form})

def rnaseq_yaml(rnaseq):
    field_dict = dict()
    field_dict['reads'] = []
    for field, value in rnaseq.__dict__.items():
        if field == 'fastqs':
            pass
        elif field in ['speciesGenomeDir', 'repeatElementGenomeDir']:
            field_dict[field] = {'class': 'Directory', 'path': value}
        elif field in ['speciesChromSizes', 'b_adapters']:
            field_dict[field] = {'class': 'File', 'path': value}
        elif field != '_state' and field != 'barcode_file' and field != 'id':
            field_dict[field] = value
    return "#!/usr/bin/env RNASEQ_singleend\n" + yaml.dump(field_dict,default_flow_style=False)

def CLIP_yaml(clip):
    # initialize new YAML file by initializing dict
    field_dict = dict()

    field_dict['samples'] = []

    # iterate through form field names
    for field, value in clip.__dict__.items():
        if field == 'fastqs':
            for i in value.split(','):
                fastq = Fastq.objects.get(pk=i)
                field_dict['samples'].append([
                    {'name': fastq.ip_title, 'read1': {'class': 'File', 'path': fastq.ip_path}, 'adapters': {'class': 'File', 'path': fastq.ip_adapter_path}},
                    {'name': fastq.sminput_title, 'read1': {'class': 'File', 'path': fastq.sminput_path}, 'adapters': {'class': 'File', 'path': fastq.sminput_adapter_path}},
                ])
        elif field in ['speciesGenomeDir', 'repeatElementGenomeDir']:
            field_dict[field] = {'class': 'Directory', 'path': value}
        elif field in ['chrom_sizes', 'blacklist_file']:
            field_dict[field] = {'class': 'File', 'path': value}
        elif field != '_state' and field != 'barcode_file' and field != 'id':
            field_dict[field] = value

    # write to YAML
    # with open(r'./output_yaml/sample_output-' + str(clip.id) + '.yaml', "w") as file:
    #     file.write("#!/usr/bin/env eCLIP_singleend\n")
    #     documents = yaml.dump(field_dict, file)

    return "#!/usr/bin/env eCLIP_singleend\n" + yaml.dump(field_dict,default_flow_style=False)


def skipper_tsv(clip):
    # initialize new YAML file by initializing dict
    rows = ','.join([
        'Experiment', 'Sample', 'Cells',
        'Input_replicate', 'Input_adapter', 'Input_fastq',
        'CLIP_replicate', 'CLIP_adapter', 'CLIP_fastq',
        '\n'
    ])
    # iterate through form field names

    for field, value in clip.__dict__.items():
        if field == 'fastqs':
            for i in value.split(','):
                fastq = Fastq.objects.get(pk=i)

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
    config_string = ""
    # iterate through form field names
    for field, value in clip.__dict__.items():
        if field == 'informative_read' or field == 'uninformative_read' or field == 'umi_size':
            config_string += f'{field.upper()} = {value}\n'
        elif field != '_state' and field != 'id' and field != 'barcode_file' and field != 'fastqs':
            config_string += f'{field.upper()} = \"{value}\"\n'
    return config_string


def index_view(request):
    context = {'LOGIN_URL': settings.LOGIN_URL}
    template = 'form_builder/index.html'
    return render(request, template, context)