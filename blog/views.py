from collections import defaultdict

from django.shortcuts import render
# include model we've written in models.py
# . before models means curr directory or current app
from .models import Post, Fastq, CLIPManifest, SkipperConfigManifest
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CLIPManifestForm, SkipperConfigManifestForm
import yaml
import pandas as pd
from django.http import HttpResponse

# Create your views here.


def post_list(request):
    # renders our template blog/post_list.html
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # request: everything we receive from the user via the Internet
    # template file path
    # {}a place in which we can add some things for the template to use
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    # all form data typed
    if request.method == "POST":
        # construct PostForm with data from the form
        form = PostForm(request.POST)
        # no incorrect values submitted
        if form.is_valid():
            # save with form.save without saving the Post model yet
            post = form.save(commit=False)
            # add author
            post.author = request.user
            # add date
            post.published_date = timezone.now()
            # preserve changes (author and date)
            post.save()
            # for every new post, create new YAML
            post_yaml(post, form)
            # go to post_detail page to see new blog post
            return redirect('post_detail', pk=post.pk)
    # blank form
    else: 
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    # get Post model we want to edit with
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # pass post as an instance when saving
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # when editing form, overwrite existing form with new YAML
            post_yaml(post, form)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_yaml(post, form):
    # initialize new YAML file by initializing dict
    post_dict = dict()
    # create key with data table name, list as value
    post_dict[post._meta.db_table] = [] 
    # create new dict
    field_dict = dict()

    # iterate through form field names
    for x in form.fields:
        # map form field values to form field names in field dict
        field_dict[str(x)] = form.cleaned_data.get(str(x))

    # append this to list mapped to db_table key
    post_dict[post._meta.db_table].append(field_dict)

    # write to YAML
    with open(r'./output_yaml/sample_output-' + str(post.id) + '.yaml', "w") as file:
        documents = yaml.dump(post_dict, file)


def CLIP_form(request):
    fastq = Fastq.objects.all().order_by('-id')[:20]  # will list the last 20

    if request.method == 'POST':
        form = CLIPManifestForm(request.POST)
        if request.POST.get("save"):
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
                file_data = CLIP_yaml(clip)
                # set variables to field values
                # return redirect('/CLIP/')
                response = HttpResponse(file_data, content_type='application/text charset=utf-8')
                f = request.POST.get('dataset', 'manifest')
                response['Content-Disposition'] = f'attachment; filename="{f}.yaml"'
                return response

        elif request.POST.get("newItem"):
            ip_fastq_path = request.POST.get("ip_fastq_path")
            ip_adapter_path = request.POST.get("ip_adapter_path")
            sminput_fastq_path = request.POST.get("sminput_fastq_path")
            sminput_adapter_path = request.POST.get("sminput_adapter_path")
            cells = request.POST.get("cells")
            experiment = request.POST.get("experiment")
            sample = request.POST.get("sample")
            ip_rep = request.POST.get("ip_rep")
            sminput_rep = request.POST.get("sminput_rep")
            Fastq.objects.create(
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
        form = CLIPManifestForm()
    return render(request, 'blog/CLIP_form.html', {'form': form, 'fastq': fastq})


def SKIPPER_form(request):
    fastq = Fastq.objects.all().order_by('-id')[:20]  # will list the last 20

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
            ip_fastq_path = request.POST.get("ip_fastq_path")
            ip_adapter_path = request.POST.get("ip_adapter_path")
            sminput_fastq_path = request.POST.get("sminput_fastq_path")
            sminput_adapter_path = request.POST.get("sminput_adapter_path")
            cells = request.POST.get("cells")
            experiment = request.POST.get("experiment")
            sample = request.POST.get("sample")
            ip_rep = request.POST.get("ip_rep")
            sminput_rep = request.POST.get("sminput_rep")
            Fastq.objects.create(
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
    return render(request, 'blog/SKIPPER_form.html', {'form': form, 'fastq': fastq})


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
    pathdict_ip = defaultdict(int)
    pathdict_input = defaultdict(int)

    repdict = defaultdict(set)
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