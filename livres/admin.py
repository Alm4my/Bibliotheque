from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from comptes.models import Utilisateur
from django.utils.translation import gettext_lazy as _


class UtilisateurAdmin(UserAdmin):
    list_display = ("matricule", "email", "nom", "prenoms", "telephone", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("matricule", "nom", "prenoms", "email")
    ordering = ("matricule",)
    fieldsets = (
        (None, {"fields": ("matricule", "password")}),
        (_("Personal info"), {"fields": ("nom", "prenoms", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("matricule", "password1", "password2"),
            },
        ),
    )


admin.site.register(Utilisateur, UtilisateurAdmin)
