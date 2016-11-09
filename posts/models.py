from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify, mark_safe
from django.db.models.signals import pre_save
from django.utils import timezone

from markdown_deux import markdown
from taggit.managers import TaggableManager

from .utils import get_read_time
from .categoryModels import Category

# Create your models here.


class PostPublishedManager(models.Manager):
    def published(self):
        return super(PostPublishedManager, self).get_queryset().filter(status='published')

    def draft(self):
        return super(PostPublishedManager, self).get_queryset().filter(status='draft')



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Roboczy'),
        ('published', 'Opublikowany'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, related_name='blog_posts')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey('posts.Category')

    tags = TaggableManager()
    objects = PostPublishedManager()


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail',
                       args=[self.slug])

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

pre_save.connect(pre_save_post_receiver, sender=Post)