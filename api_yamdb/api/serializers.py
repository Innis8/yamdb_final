import datetime as dt

from django.db.models import Avg
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(f'There is no user {value}')
        return value


class AdminSerializer(serializers.ModelSerializer):
    """Admin role"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is invalid username')
        return value


class StandartUserSerializer(serializers.ModelSerializer):
    """User role"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is invalid username')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий произведений."""

    class Meta:
        model = Category
        fields = 'name', 'slug'
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров."""

    class Meta:
        model = Genre
        fields = 'name', 'slug'
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def validate(self, data):
        slug = self.context['request'].data.get('category')
        if slug is not None:
            category = Category.objects.get(slug=slug)
            if category:
                data['category'] = category
            else:
                raise serializers.ValidationError('Категория не существует!')
        slugs = self.context['request'].data.getlist('genre')
        if len(slugs) > 0:
            genres = []
            for slug in slugs:
                genre = Genre.objects.filter(slug=slug)
                if genre:
                    genres.append(genre[0])
                else:
                    raise serializers.ValidationError('Жанр не существует!')
            data['genre'] = genres
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        title.genre.set(genres)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ("title",)
        model = Review

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                "Оценка должна быть в диапазоне от 1 до 10"
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ("review",)
        model = Comment
