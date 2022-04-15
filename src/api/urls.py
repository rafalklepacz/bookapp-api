from django.urls import path

from .views import UserView, BookView


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
    'post': 'create',
    'put': 'update'
})

urlpatterns = [
    path('books/', books_list),
    path('books/<int:pk>', books_detail),
    path('users/', users_list)
]
