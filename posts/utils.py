import re
import math

from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_list = re.findall(r'\w+', word_string)
    count = len(matching_list)
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)
    return int(read_time_min)

def deep_search_category(category):
    if category.children.count() == 0:
        yield category
    else:
        yield category
        for c in category.children.all():
            yield from deep_search_category(c)