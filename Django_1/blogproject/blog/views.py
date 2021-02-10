from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    content = {
        "post_list": post_list,

    }
    return render(request, 'blog/index.html', content)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        # 'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    content = {
        "post": post

    }
    return render(request, 'blog/detail.html', content)


def archive(request, year, month):
    # 按照年月排序查询，然后在按照创建时间的倒叙查询
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    content = {
        "post_list": post_list

    }
    return render(request, 'blog/index.html', content)


def category(request, name):
    post_list = Post.objects.filter(category__name=name).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
