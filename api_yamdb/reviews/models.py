from django.db import models

from users.models import User


CHAR_LENGTH = 30


class Category(models.Model):
    """Базвоый класс для категорий произведений."""

    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        """Вернуть название категории."""
        return self.name


class Genre(models.Model):
    """Базвоый класс для жанров."""

    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        """Вернуть название жанра."""
        return self.name


class Title(models.Model):
    """Базвоый класс для произведений."""

    name = models.CharField(verbose_name='название', max_length=50)
    year = models.PositiveSmallIntegerField(verbose_name='год издания')
    description = models.TextField(
        max_length=200,
        verbose_name='описание',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='категория',
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre, through='Genre_Title')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        """Вернуть название произведения."""
        return self.name


class Genre_Title(models.Model):
    """Класс для связи произведений и жанров."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение',
        related_name='genre_titles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='жанр',
        related_name='genre_titles',
    )

    class Meta:
        models.UniqueConstraint(
            fields=('title', 'genre'),
            name='unique_genre_title'
        )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения',
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ID автора отзыва',
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = (
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=10),
                name="Оценка должна быть от 1 до 10",
            ),
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_author_title',
            ),
        )

    def __str__(self):
        return self.text[:CHAR_LENGTH]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Прокомментированный отзыв',
        related_name='comments',
    )
    text = models.TextField('Текст комментария к отзыву')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария к отзыву',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'

    def __str__(self):
        return self.text[:CHAR_LENGTH]
