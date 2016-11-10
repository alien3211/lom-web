from django.conf.urls import url

from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
    CommentCreateAPIVIew,
)

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIVIew.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', CommentDetailAPIVIew.as_view(), name='delete'),
]
