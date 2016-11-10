from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .categoryModels import Category

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

    initial_data = {
        "content_type": post.get_content_type,
        "object_id": post.id
    }

    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid() and request.user.is_authenticated():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()


        new_comment, created = Comment.objects.get_or_create(
                                                user=request.user,
                                                content_type=content_type,
                                                object_id=obj_id,
                                                content=content_data,
                                                parent=parent_obj,
                                            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments
    context = {
        'post': post,
        'categories': cat,
        'similar_posts': similar_posts,
        "comments": comments,
        "comment_form": comment_form,
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
        if instance.status == "draft":
            return HttpResponseRedirect(reverse('posts:draft_list'))
        else:
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
        if instance.status == "draft":
            return HttpResponseRedirect(reverse('posts:draft_list'))
        else:
            return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, 'post/form.html', context)


# to update the search data you need run './manage.py update_index' commend
def post_search(request):
    form = SearchForm()
    if 'query' in request.GET and request.GET.get('query') != "":
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
    return render(request, 'post/search.html', context)


def post_category(request, id=None, path=None):
    category = get_object_or_404(Category, id=id)

    object_list = category.post_set.filter(status="published")

    paginator = Paginator(object_list, settings.POST_PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'posts': posts,
        'page': posts
    }

    return render(request, 'post/category.html', context)