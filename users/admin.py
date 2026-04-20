from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import OperationalError
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "name", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "name", "phone_number")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "id",
        "username",
        "email",
        "name",
        "phone_number",
        "is_superuser",
        "is_staff",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "username", "email")
    list_filter = ("is_active", "is_superuser", "is_staff")
    ordering = ("-id",)
    list_per_page = 10

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("name", "phone_number")} ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "name", "phone_number", "password1", "password2"),
            },
        ),
    )

    def delete_view(self, request, object_id, extra_context=None):
        """Override delete view to fallback to direct deletion when related-table queries fail.

        The admin delete confirmation page gathers related objects and can raise
        OperationalError if related tables (e.g., from new apps) don't exist yet.
        This catches that case and attempts a safe direct deletion.
        """
        try:
            return super().delete_view(request, object_id, extra_context)
        except OperationalError as exc:
            try:
                obj = self.get_queryset(request).get(pk=object_id)
                display = str(obj)
                obj.delete()
                messages.success(request, f"Deleted {display} (fallback delete).")
                return HttpResponseRedirect(reverse('admin:users_user_changelist'))
            except Exception as e:
                messages.error(request, f"Unable to delete object: {e}")
                return HttpResponseRedirect(reverse('admin:users_user_changelist'))