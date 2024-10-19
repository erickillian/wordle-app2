from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, TokenMetadata
from users.serializers import UserRegistrationSerializer


class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserRegistrationSerializer  # Ensure this form is correctly defined
    list_display = ("full_name", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("full_name", "email", "password", "color_mode", "profile_picture")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("full_name", "email", "password1", "password2"),
            },
        ),
    )
    filter_horizontal = ("user_permissions", "groups")
    ordering = ("email",)  # Updated to use a valid field in the User model


admin.site.register(User, UserAdmin)
admin.site.register(TokenMetadata)
