from sqlite3 import SQLITE_CREATE_INDEX
from django.shortcuts import render
# include model we've written in models.py
# . before models means curr directory or current app
from .models import Post#, CLIP
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CLIPForm, PostForm
import yaml

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
    if request.method == 'POST':
        form = CLIPForm(request.POST)
        if form.is_valid():
            clip = form.save(commit=False)
            description = form.cleaned_data['description']
            barcode_file = form.cleaned_data['barcode_file']
            adapter_file = form.cleaned_data['adapter_file']
            chrom_sizes = form.cleaned_data['chrom_sizes']
            star_index = form.cleaned_data['star_index']
            umi_pattern = form.cleaned_data['umi_pattern']
            fastqs = form.cleaned_data['fastqs']
            clip.save()
            CLIP_yaml(form, clip)
            # set variables to field values
            return redirect('/')
    else: 
        form = CLIPForm()
    return render(request, 'blog/CLIP_form.html', {'form': form})

def CLIP_yaml(form, clip):
    # initialize new YAML file by initializing dict
    form_dict = dict()
    field_dict = dict()

    # iterate through form field names
    for fields in form.fields:
        print(form.cleaned_data.get(fields))
        field_dict[fields] = form.cleaned_data.get(fields)
        
    form_dict['CLIP_Form'] = field_dict
    # write to YAML
    with open(r'./output_yaml/sample_output-' + str(clip.id) + '.yaml', "w") as file:
        documents = yaml.dump(form_dict, file)

