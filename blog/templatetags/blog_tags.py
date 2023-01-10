import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from shop.products.models import ProductCategory
from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('includes/recent_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('includes/blog_sidebar.html')
def show_blog_sidebar(count=3):
    categories = ProductCategory.objects.all()
    recent_posts = Post.published.order_by('-publish')[:count]
    return {
        'categories': categories,
        'recent_posts': recent_posts,
    }


@register.simple_tag
def get_most_recent_posts(count=3):
    return Post.published.order_by('-publish')[:count]


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
