# 自定义模板标签
from django import template
from ..models import Post,Tag,Category
from django.db.models.aggregates import Count
register = template.Library()
#修饰该模板
@register.inclusion_tag('My_Blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.all().order_by('-created_time')[:num]
    }
##
@register.inclusion_tag('My_Blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }
##
@register.inclusion_tag('My_Blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }
##
@register.inclusion_tag('My_Blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }