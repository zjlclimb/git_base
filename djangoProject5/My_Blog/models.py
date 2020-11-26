import re 
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from markdown.extensions.toc import TocExtension, slugify


class Category(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}


class Post(models.Model):
    title = models.CharField(max_length=200,verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    # 一对多
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='分类')
    #多对多
    tag = models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    # 一篇文章只能有一个作者，而一个作者可以有多篇文章，所以为一对多
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='作者')
    created_time = models.DateTimeField(verbose_name='创作时间',default=timezone.now)#自动保存首次创建模型的时间
    modified_time = models.DateTimeField(verbose_name='修改时间')
    excerpt = models.CharField(max_length=50,blank=True)
    #记录浏览量
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('My_Blog:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    # 写一个方法记录浏览量
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

