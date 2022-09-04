from django.contrib import admin

from reviews.models import Review, Category, Genre, Genre_Title, Title, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'text', 'pub_date')


admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Genre_Title)
admin.site.register(Title)
admin.site.register(Comment, CommentAdmin)
