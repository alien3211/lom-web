from django import forms

from .models import Post
from pagedown.widgets import PagedownWidget


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(forms.ModelForm):
    DATEPICKER = {
        'type': "text",
        'name': "daterange",
        'value': "01/01/2015 - 01/31/2015",
    }
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.widgets.Input(attrs=DATEPICKER))

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "status",
            "publish",
            "category",
            "tags",
        ]