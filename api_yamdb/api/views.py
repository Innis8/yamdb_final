from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ValidationError

from reviews.models import Category, Comment, Genre, Title, Review
from api.filters import TitleFilter
from api.permissions import (
    IsAdminOrListOnly, IsAdminOrReadOnly, AuthorOrAdminOrReadOnly)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    TitleSerializer, ReviewSerializer)


class CreateListDestroyViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Вьюсет, который позволяет только GET, POST и DELETE запросы."""

    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для просмотра категорий произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrListOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для просмотра жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrListOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра отзывов."""

    permission_classes = [AuthorOrAdminOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        user_review_list = user.reviews.all()
        user_review_title_id_list = user_review_list.values_list(
            'title_id',
            flat=True
        )
        if int(title_id) in user_review_title_id_list:
            raise ValidationError(
                "Вы уже оставили отзыв на это произведение."
            )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра комментариев."""

    permission_classes = [AuthorOrAdminOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(
            author=self.request.user,
            review=review
        )
