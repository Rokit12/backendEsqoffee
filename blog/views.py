from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.views.generic import ListView

from taggit.models import Tag

from .models import Post, PostCategory
from .forms import CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/index.html'


def post_list(request, tag_slug=None):
    template = 'blog/index.html'

    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts,
        'tag': tag,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'

    categories = PostCategory.objects.all()
    post = get_object_or_404(Post, id=post_id, status='published')

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    new_comment = CommentForm()

    context = {
        'categories': categories,
        'post': post,
        'comments': comments,
        'comment_form': new_comment,
        'new_comment': new_comment,
        'similar_posts': similar_posts
    }

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return render(request, template, context)
    else:
        comment_form = CommentForm()

    context['comment_form'] = comment_form

    return render(request, template, context)
