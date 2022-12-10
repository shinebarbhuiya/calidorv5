from django.contrib import admin
from django.urls import path

from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('blog_topic/', views.blog_topic_generator, name='blog_topic_generator'),
    path('blog_section/', views.blog_sections, name='blog_section'),
    path('delete-blog-topic/<str:uniqueId>/', views.delete_blog_topic, name='delete_blog_topic'),
    path('createBlogFromTopic/<str:uniqueId>/', views.createBlogFromTopic, name='createBlogFromTopic'),
    
    # saving the blog topic for future use
    path('save_topic/<str:blogTopic>/', views.save_topic, name='save_topic'),
    path('use_topic/<str:blogTopic>/', views.use_topic, name='use_topic'),
    path('view_generated_blog/<slug:slug>/', views.view_generated_blog, name='view_generated_blog'),
    
 
]
