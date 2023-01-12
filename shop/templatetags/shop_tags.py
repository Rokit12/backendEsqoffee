from django import template
from ..models import Shop, ShopStory, ShopTestimonial

register = template.Library()


@register.inclusion_tag('includes/discover_story.html')
def show_story():
    story = ShopStory.objects.all()
    if story.count() > 0:
        story = story[0]
        return {'story': story}
    return {'story': story}


@register.inclusion_tag('includes/footer_about.html')
def show_footer_about():
    story = ShopStory.objects.all()
    if story.count() > 0:
        story = story[0]
        return {'story': story}
    return {'story': story}


@register.inclusion_tag('includes/discover_testimonials.html')
def show_testimonials():
    testimonials = ShopTestimonial.objects.all()
    return {'testimonials': testimonials}
