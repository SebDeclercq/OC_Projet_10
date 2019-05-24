from typing import Sequence, Type
from django.contrib import admin
from .models import User
from .forms import AdminForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form: Type[AdminForm] = AdminForm
    list_display: Sequence[str] = ('email', 'name', 'firstname', 'is_active',
                                   'is_staff',)
    list_filter: Sequence[str] = ('is_active', 'is_staff', 'is_superuser',)
    search_fields: Sequence[str] = ('email', 'name',)
    ordering: Sequence[str] = ('email', 'name', 'firstname',)
