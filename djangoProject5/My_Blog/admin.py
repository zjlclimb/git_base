from django.contrib import admin
from My_Blog.models import Post,Tag,Category
# Register your models here
class Post_Admin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tag']
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post,Post_Admin)
admin.site.register(Tag)
admin.site.register(Category)
