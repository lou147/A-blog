from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'updated', 'timestamp']
    list_filter = ['category', 'title', 'updated']
    search_fields = ['title', 'content', 'category']
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)




