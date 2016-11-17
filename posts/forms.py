from django import forms

from .models import Post
from pagedown.widgets import PagedownWidget


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(forms.ModelForm):
    DATEPICKER = {
        'type': "text",
    }
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateTimeField(widget=forms.widgets.Input(attrs=DATEPICKER))

    def __init__(self, *args, publish_disabled=False, **kwargs ):
        super(PostForm, self).__init__(*args, **kwargs)

        if publish_disabled:
            self.fields['publish'].widget.attrs['readonly'] = True


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