from django.db import models
from django.utils import timezone
# Create your models here.
##创建评论类，以及属性
class Comments(models.Model):
    name = models.CharField('名字',max_length=25)
    email = models.CharField('邮箱地址',max_length=50)
    url = models.URLField('网址',blank=True)#可以为空
    text = models.TextField('评论内容')
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    post = models.ForeignKey('My_Blog.Post',verbose_name='文章',on_delete=models.CASCADE)#实现一对一外键，链接到Post类的post文章

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name #当为复数的时候，同verbose_name（单复数一致）

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])