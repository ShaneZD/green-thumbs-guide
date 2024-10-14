from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ForumPost, Comment
from .forms import ForumPostForm, CommentForm

# Renders the forum homepage with all posts ordered by creation date.
def forum_home(request):
    posts = ForumPost.objects.all().order_by('-created_at')
    return render(request, 'forum/forum_home.html', {'posts': posts})

# Allows a logged-in user to create a new forum post.
@login_required
def create_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the post's author to the current user
            post.save()
            return redirect('forum:forum_home')
    else:
        form = ForumPostForm()
    return render(request, 'forum/create_post.html', {'form': form})

# Renders the detail view of a specific post, including its comments.
def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.comments.all()  # Fetch all comments related to the post
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Set the comment's author to the current user
            comment.post = post  # Associate the comment with the post
            comment.save()
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments, 'form': form})
