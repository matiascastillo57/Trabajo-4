from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permiso personalizado: Solo permite acceso a usuarios con rol 'admin'
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        try:
            usuario = request.user.usuario
            return usuario.rol == 'admin' and usuario.activo
        except:
            return False
