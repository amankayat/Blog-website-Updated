
from django.urls import path
from .import views


urlpatterns = [
    path('',views.BlogList.as_view(),name = "blog_list"),
    path('write/',views.CreateBlog.as_view(),name = "createblog"),
    path('details/<int:slug>',views.blog_details,name = "blog_details"),
    path('liked/<int:pk>',views.liked,name = "liked_post"),
    path('unliked/<int:pk>',views.unlike,name = "unliked_post"),
    path('myblog/',views.MyBlog.as_view(),name = "myblog"),
    path('editblog/<int:pk>',views.updateBlog.as_view(),name = "edit_blog"),
   
]
