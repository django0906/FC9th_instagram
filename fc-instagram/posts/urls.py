from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('',
         views.post_list,
         name='post_list'),
    path('upload/',
         views.post_create,
         name='post_create'),
    path('<int:post_pk>/comments/create/',
         views.comment_create,
         name='comment_create'),
    path('tag_search/',
         views.tag_search,
         name='tag_search'),
]
