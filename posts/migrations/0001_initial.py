# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 09:51
from __future__ import unicode_literals

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('thumbnail', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='uploads/categories/thumbnails')),
                ('thumbnail_width', models.IntegerField(blank=True, null=True)),
                ('thumbnail_height', models.IntegerField(blank=True, null=True)),
                ('order', models.IntegerField(default=0)),
                ('alternate_title', models.CharField(blank=True, default='', help_text='An alternative title to use on pages with this category.', max_length=100)),
                ('alternate_url', models.CharField(blank=True, help_text='An alternative URL to use instead of the one derived from the category hierarchy.', max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('meta_keywords', models.CharField(blank=True, default='', help_text='Comma-separated keywords for search engines.', max_length=255)),
                ('meta_extra', models.TextField(blank=True, default='', help_text='(Advanced) Any additional HTML to be placed verbatim in the &lt;head&gt;')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='posts.Category', verbose_name='parent')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'verbose_name_plural': 'categories',
            },
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('read_time', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'Roboczy'), ('published', 'Opublikowany')], default='draft', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('parent', 'name')]),
        ),
    ]
