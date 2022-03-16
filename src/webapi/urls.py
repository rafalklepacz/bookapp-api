from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import PublisherView

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('publishers/', PublisherView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('publishers/<int:pk>', PublisherView.as_view({'get': 'retrieve'}))
]
