from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'role', 'confirmation_code']


admin.site.register(User, CustomUserAdmin)
