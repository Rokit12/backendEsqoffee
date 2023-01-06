from django.contrib import admin
from .models import Post, PostComment, PostCategory

admin.site.register(PostComment)
admin.site.register(Post)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name']
    prepopulated_fields = {'slug': ('name',)}
