# core/permissions.py  (ou qualidade/permissions.py)

from rest_framework.permissions import BasePermission

class HasCustomPermission(BasePermission):
    """
    Checa permissões do usuário igual CheckPermissionMixin, mas para API.
    """
    permission_codename = []

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Pega codenames definidos na View
        perms = getattr(view, 'permission_codename', [])
        if not isinstance(perms, list):
            perms = [perms]

        perms_full = []
        for p in perms:
            if '.' not in p:
                app_label = view.queryset.model._meta.app_label
                perms_full.append(f"{app_label}.{p}")
            else:
                perms_full.append(p)

        if user.is_superuser:
            return True

        return user.has_perms(perms_full)
