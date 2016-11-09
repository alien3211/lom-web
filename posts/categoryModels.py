from django.db import models
from categories.models import CategoryBase, STORAGE
from django.utils.encoding import force_text
from django.urls import reverse


class Category(CategoryBase):
    thumbnail = models.FileField(
        upload_to='uploads/categories/thumbnails',
        null=True, blank=True,
        storage=STORAGE(),)
    thumbnail_width = models.IntegerField(blank=True, null=True)
    thumbnail_height = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(default=0)
    alternate_title = models.CharField(
        blank=True,
        default="",
        max_length=100,
        help_text="An alternative title to use on pages with this category.")
    alternate_url = models.CharField(
        blank=True,
        max_length=200,
        help_text="An alternative URL to use instead of the one derived from "
                  "the category hierarchy.")
    description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(
        blank=True,
        default="",
        max_length=255,
        help_text="Comma-separated keywords for search engines.")
    meta_extra = models.TextField(
        blank=True,
        default="",
        help_text="(Advanced) Any additional HTML to be placed verbatim "
                  "in the &lt;head&gt;")

    def get_absolute_url(self):
        ancestors = list(self.get_ancestors()) + [self, ]
        return reverse('posts:category', args=[self.id, '/'.join([force_text(i.slug) for i in ancestors])])

    @property
    def path_name_category_list(self):
        ancestors = self.get_ancestors()
        return [force_text(i.name) for i in ancestors] + [self.name, ]

    @property
    def path_category_list(self):
        return list(self.get_ancestors()) + [self,]

    @property
    def root(self):
        return self.get_root()

    def save(self, *args, **kwargs):
        if self.thumbnail:
            from django.core.files.images import get_image_dimensions
            import django
            if django.VERSION[1] < 2:
                width, height = get_image_dimensions(self.thumbnail.file)
            else:
                width, height = get_image_dimensions(self.thumbnail.file, close=True)
        else:
            width, height = None, None

        self.thumbnail_width = width
        self.thumbnail_height = height

        super(Category, self).save(*args, **kwargs)

    class Meta(CategoryBase.Meta):
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ('order', 'name')
