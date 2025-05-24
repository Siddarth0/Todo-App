from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm, SignupForm
from django.contrib.auth.forms import AuthenticationForm

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'media_app/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('media_app:post_list')
    return render(request, 'media_app/post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')
    likes = post.likes.count()
    form = CommentForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return redirect('media_app:post_detail', pk=pk)
    return render(request, 'media_app/post_detail.html', {'post':post,'comments':comments,'likes':likes,'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user: return redirect('media_app:post_list')
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('media_app:post_detail', pk=pk)
    return render(request, 'media_app/post_form.html', {'form':form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect('media_app:post_list')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created: obj.delete()
    return redirect('media_app:post_detail', pk=pk)

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user: return redirect('media_app:post_list')
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('media_app:post_detail', pk=comment.post.pk)
    return render(request, 'media_app/comment_form.html', {'form':form})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.user == request.user:
        comment.delete()
    return redirect('media_app:post_detail', pk=post_pk)

def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('media_app:post_list')
    return render(request, 'media_app/signup.html', {'form':form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('media_app:post_list')
    return render(request, 'media_app/login.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('media_app:post_list')
