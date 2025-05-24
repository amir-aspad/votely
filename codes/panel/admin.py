from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .forms import UserChangeForm, UserCreateForm
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    can_delete  = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        (None, {'fields': ('phone', 'email', 'username', 'password')}),
        ('permissions', {'fields': ('groups', 'user_permissions', 'is_admin', 'is_superuser', 'is_active')}),
        ('other', {'fields': ('is_email_verified', 'is_phone_verified')})
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'username', 'email', 'password', 'password2')}),
    )


    filter_horizontal = ('groups', 'user_permissions')
    inlines = (ProfileInline,)
    search_fields = ('phone', 'username', 'email')
    list_display =  ('phone', 'email', 'username', 'is_active')
    list_filter = ('is_active', 'is_superuser', 'is_email_verified', 'is_phone_verified')
    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True

        return form