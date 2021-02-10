from django.contrib import admin
from .models import Post, Tag, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'summary', 'category', 'tag']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
