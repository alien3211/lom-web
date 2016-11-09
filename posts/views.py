from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Post
from categories.models import Category

from haystack.query import SearchQuerySet

from .forms import PostForm, SearchForm
from taggit.models import Tag


# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.objects.published()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # Pagination
    paginator = Paginator(object_list, settings.POST_PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'page': posts,
        'tag': tag,
    }
    return render(request, 'post/list.html', context)


def post_draft_list(request):
    if not request.user.is_active:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404

    object_list = Post.objects.draft().filter(author=request.user)

    # Pagination
    paginator = Paginator(object_list, settings.POST_PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'page': posts,
    }
    return render(request, 'post/draft_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    cat = Category.objects.all().filter(level=0)

    # list similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.published().filter(tags__in=post_tags_ids)\
                                            .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]
    context = {
        'post': post,
        'categories': cat,
        'similar_posts': similar_posts,
    }

    return render(request, 'post/detail.html', context)


def post_create(request):
    if not request.user.is_active:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        form.save_m2m()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, 'post/form.html', context)


def post_update(request, slug=None):
    if not request.user.is_active:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    if instance.author != request.user:
        raise Http404
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, 'post/form.html', context)


# to update the search data you need run './manage.py update_index' commend
def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post)\
                      .filter(content=cd['query']).load_all()
            # count whole posts
            total_results = results.count()
            context = {
                'form': form,
                'cd': cd,
                'results': results,
                'total_results': total_results
            }
    else:
        context = {
            'form': form,
        }
    return  render(request, 'post/search.html', context)