from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html')
def show_archives():
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),

        # order='DESC' 降序排列参数
    }


@register.inclusion_tag('blog/inclusions/_categories.html')
def show_categories():
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tags.html')
def show_tags():
    return {
        'tag_list': Tag.objects.all(),
    }
