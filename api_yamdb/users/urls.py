from django.urls import path

from .views import GetTokenAPI, SignUpAPI


urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('token/', GetTokenAPI.as_view(), name='token'),
]
