from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField(model_attr='publish')
    author = indexes.CharField(model_attr='author')
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    category = indexes.CharField(model_attr='category')
    tags = indexes.CharField(use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.published()
