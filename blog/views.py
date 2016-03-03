from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
    return render(request, 'blog/post_list.html', {"posts":posts})

def post_drafts(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("-created_date")
    return render(request, 'blog/post_drafts.html', {"posts":posts})

def post_detail(request, pk):
    # post = Post.objects.get(pk=post_id) - This works, but would return a gnarly error if post_id doesn't exist!
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now() - Taking this out to implement a draft post queue, put back in to auto-publish drafts!
            post.save()
            return redirect("post_detail", pk=post.pk)      
    else:
        form = PostForm()    
    return render(request, "blog/post_edit.html", {"form": form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form":form})
   