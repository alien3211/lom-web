from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from .models import Post


class LatestPostFeed(Feed):
    title_template = 'LOM'
    link = '/post/'
    description = 'Nowe posty na LOM'

    def items(self):
        return Post.objects.published()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(item.get_markdown(), 30)