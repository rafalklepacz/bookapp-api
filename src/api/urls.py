from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import UserView, PublisherView, AuthorView, BookView


publishers_list = PublisherView.as_view({
    'get': 'list',
    'post': 'create'
})

publishers_detail = PublisherView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

authors_list = AuthorView.as_view({
    'get': 'list',
    'post': 'create'
})

authors_detail = AuthorView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

books_list = BookView.as_view({
    'get': 'list',
    'post': 'create'
})

books_detail = BookView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

users_list = UserView.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = [
    path('publishers/', publishers_list),
    path('publishers/<int:pk>', publishers_detail),
    path('authors/', authors_list),
    path('authors/<int:pk>', authors_detail),
    path('books/', books_list),
    path('books/<int:pk>', books_detail),
    path('users/', users_list)
]
