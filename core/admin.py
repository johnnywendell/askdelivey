
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Usuario,
)


"""
=========================================================
INLINE PERFIL
=========================================================
"""

class UsuarioInline(admin.StackedInline):

    model = Usuario

    can_delete = False

    extra = 0

    fk_name = 'user'


"""
=========================================================
CUSTOM USER ADMIN
=========================================================
"""

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    inlines = [UsuarioInline]

    ordering = ['id']

    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'get_tipo',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'perfil__tipo',
    )

    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )

    readonly_fields = (
        'last_login',
        'date_joined',
    )

    fieldsets = (

        (
            'Login',
            {
                'fields': (
                    'email',
                    'username',
                    'password',
                )
            }
        ),

        (
            'Informações Pessoais',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'telefone',
                )
            }
        ),

        (
            'Permissões',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),

        (
            'Datas',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )

    add_fieldsets = (

        (
            None,
            {
                'classes': ('wide',),

                'fields': (
                    'email',
                    'username',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'telefone',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )

    def get_tipo(self, obj):

        try:
            return obj.perfil.tipo

        except:
            return '-'

    get_tipo.short_description = 'Tipo'


"""
=========================================================
ADMIN PERFIL
=========================================================
"""

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'tipo',
        'telefone_verificado',
        'email_verificado',
        'ativo',
        'criado_em',
    )

    list_filter = (
        'tipo',
        'ativo',
        'telefone_verificado',
        'email_verificado',
    )

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
    )

    readonly_fields = (
        'criado_em',
        'atualizado_em',
    )

