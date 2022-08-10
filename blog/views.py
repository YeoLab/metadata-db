from django.shortcuts import render
# include model we've written in models.py
# . before models means curr directory or current app
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
import yaml

# Create your views here.

# initialize empty dictionary (should i use a constructor?)
dict_file = {}
dict_file['blog_post'] = []

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
            make_yaml(post)
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
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def make_yaml(post):
    # create new dict
            post_dict = {}
            # update values at 'title' and 'text' key
            post_dict['title'] = post.title
            post_dict['text'] = post.text
            # add this dict to list stored in 'blog_post' key
            dict_file['blog_post'].append(post_dict)
            # write to yaml
            with open(r'./output_yaml/sample_output.yaml', "w") as file:
                documents = yaml.dump(dict_file, file)
            # for debugging
            #print(dict_file)

def edit_yaml(post):
    # not sure how to find index to assess this specific dict in array 
    # perhaps create hashmap: title-> index? idk

    with open(r'./output_yaml/sample_output.yaml', "w") as file:
        documents = yaml.dump(dict_file, file)   