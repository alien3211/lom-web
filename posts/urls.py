from django.conf.urls import url, include
from . import views
from .feeds import LatestPostFeed



urlpatterns = [
    url(r'^$', views.post_list, name='main-page'),
    url(r'^$', views.post_list, name='list'),
    url(r'^draft/$', views.post_draft_list, name='draft_list'),
    url(r'^feed/$', LatestPostFeed(), name='feed'),
    url(r'^search/$', views.post_search, name='search'),
    url(r'^category/$', views.list_category, name='list_category'),
    url(r'^category/create/$', views.create_category, name='create_category'),
    url(r'^category/(?P<id>\d+)/(?P<path>.*)$', views.post_category, name='category'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.post_list, name='list_by_tag'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^post/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', views.post_update, name='edit'),
]