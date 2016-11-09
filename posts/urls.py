from django.conf.urls import url, include
from . import views
from .feeds import LatestPostFeed



urlpatterns = [
    url(r'^$', views.post_list, name='main-page'),
    url(r'^$', views.post_list, name='list'),
    url(r'^draft/$', views.post_draft_list, name='draft_list'),
    url(r'feed/$', LatestPostFeed(), name='post_feed'),
    url(r'search/$', views.post_search, name='post_search'),
    url(r'^category/$', views.post_list, name='category_list'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.post_list, name='list_by_tag'),
    url(r'^post/create/$', views.post_create, name='create'),
    url(r'^post/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', views.post_update, name='edit'),
    # url(r'^category/(?P<path>.+)/$', post_detail, name='category_detail'),
]