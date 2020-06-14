from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from posts.forms import CommentForm, PostForm
from posts.models import Group, Post, User


def get_paginator_context(posts_list, page_slice, request) -> dict:
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return context


def page_not_found(request, exception):
    return render(request, "misc/404.html",
                  {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@cache_page(20 * 60)
def index(request):
    posts_list = Post.objects.all()
    context = get_paginator_context(posts_list, 10, request)
    return render(request, 'index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    context = {'group': group}
    context.update(get_paginator_context(posts_list, 10, request))
    return render(request, 'group.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.all()

    context = {
        'author': author,
        'is_follow': author.following.contains(request.user),
    }
    context.update(get_paginator_context(posts_list, 10, request))
    return render(request, 'profile.html', context)


def post_detail(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(author.posts, pk=post_id)
    form = CommentForm()
    is_follow = author.following.contains(request.user)

    context = {
        'author': author,
        'post': post,
        'form': form,
        'is_follow': is_follow,
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(author.posts, pk=post_id)

    if post.author != request.user:
        return redirect('post_view', author.username, post.id)

    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post_view', username, post.id)

    context = {'form': form, 'post': post}
    return render(request, 'new_post.html', context)


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {'form': form})

    context = {'form': form}
    return render(request, 'new_post.html', context)


@login_required
def add_comment(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(author.posts, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

    return redirect('post_view', username, post.id)


@login_required
def follow_index(request):
    posts_list = request.user.follower.posts()
    context = get_paginator_context(posts_list, 10, request)
    return render(request, 'follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    author.following.append(request.user)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    request.user.follower.remove(author)
    return redirect('profile', username)


@login_required
def profile_follow_switch(request, username):
    # Из-за тестов отложу функцию до лучших времен. Она заменит две выше
    author = get_object_or_404(User, username=username)
    author.following.switch(request.user)
    return redirect('profile', username)
