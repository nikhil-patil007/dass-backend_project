from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name',"last_name", "username", "phone_number", "is_superuser", "created_at", "updated_at")
    list_display_links  = ('id', 'first_name',"last_name", "username", "phone_number", "is_superuser", "created_at", "updated_at")
    list_filter = ('is_active',)
    ordering = ('-id',)
    list_per_page = 10