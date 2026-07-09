import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Post, Comment, Like, Follow, Profile
from .forms import RegisterForm, PostForm, CommentForm, ProfileEditForm


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(
        Q(user__in=following_ids) | Q(user=request.user)
    ).select_related('user', 'user__profile').prefetch_related('likes', 'comments').order_by('-created_at')

    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    suggested_users = User.objects.exclude(
        Q(id=request.user.id) | Q(id__in=following_ids)
    ).select_related('profile').order_by('?')[:5]

    post_form = PostForm()
    return render(request, 'social/home.html', {
        'posts': posts,
        'liked_post_ids': list(liked_post_ids),
        'suggested_users': suggested_users,
        'post_form': post_form,
    })


def explore(request):
    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(content__icontains=query) | Q(user__username__icontains=query)
        ).select_related('user', 'user__profile').prefetch_related('likes', 'comments')
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).exclude(id=request.user.id).select_related('profile')[:10]
    else:
        posts = Post.objects.all().select_related('user', 'user__profile').prefetch_related('likes', 'comments').order_by('-created_at')
        users = []

    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'social/explore.html', {
        'posts': posts,
        'users': users,
        'query': query,
        'following_ids': list(following_ids),
        'liked_post_ids': list(liked_post_ids),
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'social/register.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).select_related('user', 'user__profile').prefetch_related('likes', 'comments')
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    followers = Follow.objects.filter(following=user).select_related('follower', 'follower__profile')[:6]
    following = Follow.objects.filter(follower=user).select_related('following', 'following__profile')[:6]

    return render(request, 'social/profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'liked_post_ids': list(liked_post_ids),
        'followers': followers,
        'following': following,
    })


@login_required
def edit_profile(request, username):
    if request.user.username != username:
        return redirect('profile', username=username)
    profile_obj = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.save()
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileEditForm(instance=profile_obj, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
    return render(request, 'social/edit_profile.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('user', 'user__profile').all()
    is_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': form,
        'is_liked': is_liked,
    })


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('home')


@login_required
@require_POST
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('post_detail', post_id=post_id)


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes_count()})


@login_required
@require_POST
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
        following = False
    else:
        following = True

    return JsonResponse({
        'following': following,
        'followers_count': target_user.profile.followers_count(),
    })


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        qs = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).exclude(id=request.user.id)[:8]
        for u in qs:
            users.append({
                'username': u.username,
                'display_name': u.get_full_name() or u.username,
                'url': f'/profile/{u.username}/',
            })
    return JsonResponse({'users': users})
