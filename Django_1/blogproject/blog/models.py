from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "种类"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class PostQuerySet(models.QuerySet):  # 自定义模型管理器

    def published(self):
        return self.filter(created_time__lte=timezone.now())


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    summary = models.TextField(max_length=200, blank=True)
    created_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    author = models.CharField(max_length=20, default='阿波卡多')

    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.summary = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
