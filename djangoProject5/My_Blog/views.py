from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect
from pure_pagination.mixins import PaginationMixin

from My_Blog.models import Post,Category,Tag
from django.views.generic import  ListView,DetailView
from django.contrib import messages

# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, template_name='My_Blog/index.html', context={'post_list':post_list})
#将上述视图函数改为类视图
class IndexView(ListView,PaginationMixin):
    model = Post
    template_name = 'My_Blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     #阅读量增加1
#     post.increase_views()
#
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#     return render(request, 'My_Blog/detail.html', context={'post': post})
#将上述视图函数改为类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'My_Blog/detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response
    # def get_object(self, queryset=None):
    #     # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         # 记得在顶部引入 TocExtension 和 slugify
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)
    #     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''
    #     return post

#使用时间归档filter来过滤文章
# def archive(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request, 'My_Blog/index.html', context={'post_list': post_list})
##使用类函数来改写上述视图函数
class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year=year, created_time__month=month)


# #使用分类归档filter来过滤文章
# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request,'My_Blog/index.html',context={'post_list':post_list})
#使用类函数来改写上述视图函数
class CategoryView(ListView):
    model = Post
    template_name = 'My_Blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)


#使用标签归档filter来过滤文章
# def tag(request,pk):
#     t = get_object_or_404(Tag,pk=pk)
#     post_list = Post.objects.filter(tag=t).order_by('-created_time')
#     return render(request,'My_Blog/index.html',context={'post_list':post_list})
#使用类函数来改写上述视图函数
class TagView(ListView):
    model = Post
    template_name = 'My_Blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        t = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tag=t)

##创建一个视图函数，实现全文搜索
def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = '请输入关键词'
        messages.add_message(request,messages.ErrOR,error_msg,extra_tags='danger')
        return redirect('My_Blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'My_Blog/index.html', {'post_list': post_list})

