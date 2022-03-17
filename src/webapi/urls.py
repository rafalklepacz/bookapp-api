from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import PublisherView

publishers_list = PublisherView.as_view({
    'get': 'list',
    'post': 'create'
})

publishers_detail = PublisherView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('publishers/', publishers_list),
    path('publishers/<int:pk>', publishers_detail)
]
