from django.contrib import admin

from .models import Post, Category
from categories.admin import CategoryBaseAdmin, CategoryBaseAdminForm
from django.utils.translation import ugettext_lazy as _

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'category')
    list_filter = ('status', 'timestamp', 'publish', 'author', 'updated')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


class CategoryAdminForm(CategoryBaseAdminForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_alternate_title(self):
        if self.instance is None or not self.cleaned_data['alternate_title']:
            return self.cleaned_data['name']
        else:
            return self.cleaned_data['alternate_title']


class CategoryAdmin(CategoryBaseAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'alternate_title', 'active')
    fieldsets = (
        (None, {
            'fields': ('parent', 'name', 'thumbnail', 'active')
        }),
        (_('Meta Data'), {
            'fields': ('alternate_title', 'alternate_url', 'description',
                       'meta_keywords', 'meta_extra'),
            'classes': ('collapse',),
        }),
        (_('Advanced'), {
            'fields': ('order', 'slug'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)