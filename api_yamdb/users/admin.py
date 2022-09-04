from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'role', 'is_staff', 'is_active',
        'date_joined', 'last_login', 'email', 'first_name', 'last_name',
        'bio',
    )


admin.site.register(User, UserAdmin)
