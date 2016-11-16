from django import template

from posts.categoryModels import Category
from posts.models import Post

register = template.Library()



@register.simple_tag
def total_posts():
    return Post.objects.published().count()


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()


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


@register.inclusion_tag('tree_view.html')
def list_category_toggle_menu():
    categories = Category.objects.all().filter(level=0)
    return {'categories': categories}

