from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


def index(request):
    posts_list = Post.objects.all()  # .order_by("-timestamp")

    paginator = Paginator(posts_list, 5)
    page_var = 'page1'
    page = request.GET.get(page_var)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'List of Posts',
        'posts': posts,
        'page_var': page_var
    }

    return render(request, 'blog/index.html', context)
