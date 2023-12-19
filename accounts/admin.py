from django.contrib import admin

from .models import CustomUser


class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "role", "is_verified", "is_superuser")


admin.site.register(CustomUser, CustomUserModelAdmin)
