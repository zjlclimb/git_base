from django.urls import path
from . import views,models
from My_Blog.feeds import AllPostsRssFeed
app_name = 'My_Blog'

urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),#使用.as_view函数来引用类函数IndexView
    #根据views中post加文章id来添加urls
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='detail'),
    #为view中根据文章时间:created_time来filter过滤，添加urls
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    #为views中category的过滤信息来添加
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #为views中Tag的过滤信息来添加
    path('tags/<int:pk>/',views.TagView.as_view(),name='tag'),
    #为全文搜索添加url
    path('search/', views.search, name='search'),


    ##以下方式存疑，不推荐，硬编码
    path('index.html',views.IndexView.as_view(),name='index'),
    # path('full-width.html',views.index,name='index'),
    # path('about.html',views.index,name='index'),
    # path('contact.html',views.index,name='index'),
]
