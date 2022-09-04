from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import AdminDataAPI, UserDataAPI
from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet)


app_name = 'api'

router = SimpleRouter()
router.register('users', AdminDataAPI, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', UserDataAPI.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
