from django import template

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.objects.published().count()

@register.inclusion_tag('post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.published().order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('post/categories_link.html')
def categories_to_html_link(post_categories):
    return {'categories': post_categories.path_category_list}

@register.inclusion_tag('post/tags_link.html')
def tags_to_html_link(post_tags):
    return {'tags': post_tags.all()}
