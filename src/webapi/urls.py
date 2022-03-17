from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import PublisherView, AuthorView, BookView

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

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('publishers/', publishers_list),
    path('publishers/<int:pk>', publishers_detail),
    path('authors/', authors_list),
    path('authors/<int:pk>', authors_detail),
    path('books/', books_list),
    path('books/<int:pk>', books_detail)
]
