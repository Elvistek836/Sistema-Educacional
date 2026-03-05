from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Profesor, Alumnos

def role_required(allowed_roles):
    """
    Decorador para restringir el acceso a vistas basado en el rol del usuario.
    
    Args:
        allowed_roles: Lista de roles permitidos (DIRECTOR, PROFESOR, ALUMNO, etc.)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = getattr(request, 'user', None)
            is_auth = (user and user.is_authenticated) or bool(request.session.get('nomUsuario'))
            if not is_auth:
                messages.error(request, "Debe iniciar sesión para acceder a esta página")
                return redirect('/login')
            user_role = request.session.get('cargoUsuario')
            if not user_role:
                if user and user.is_superuser:
                    user_role = 'ADMINISTRADOR'
                elif user:
                    grp = user.groups.first()
                    user_role = grp.name if grp else None
            if (user_role and user_role in allowed_roles) or (user and user.groups.filter(name__in=allowed_roles).exists()):
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tiene permisos para acceder a esta página")
            return redirect('/menu')
        
        return _wrapped_view
    
    return decorator

def profesor_data_only(view_func):
    """
    Decorador para asegurar que los profesores solo vean su propia información.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.session.get('nomUsuario'):
            messages.error(request, "Debe iniciar sesión para acceder a esta página")
            return redirect('/')
            
        # Obtener el cargo del usuario
        cargo_usuario = request.session.get('cargoUsuario')
        
        # Si es DIRECTOR o SECRETARIA, permitir acceso completo
        if cargo_usuario in ['DIRECTOR', 'SECRETARIA']:
            return view_func(request, *args, **kwargs)
            
        # Si es PROFESOR, verificar que solo acceda a sus datos
        if cargo_usuario == 'PROFESOR':
            # Obtener el email del usuario
            email_usuario = request.session.get('nomUsuario')
            
            # Buscar el profesor por email
            profesor = Profesor.objects.filter(email=email_usuario).first()
            
            if profesor:
                # Si hay un ID de profesor en los kwargs, verificar que sea el suyo
                if 'profesor_id' in kwargs and str(kwargs['profesor_id']) != str(profesor.id):
                    messages.error(request, "No tiene permisos para acceder a esta información")
                    return redirect('/menu')
                
                # Añadir el profesor actual al request para filtrar en la vista
                request.profesor_actual = profesor
            
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def alumno_data_only(view_func):
    """
    Decorador para asegurar que los alumnos solo vean su propia información.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.session.get('nomUsuario'):
            messages.error(request, "Debe iniciar sesión para acceder a esta página")
            return redirect('/')
            
        # Obtener el cargo del usuario
        cargo_usuario = request.session.get('cargoUsuario')
        
        # Si es DIRECTOR o SECRETARIA, permitir acceso completo
        if cargo_usuario in ['DIRECTOR', 'SECRETARIA']:
            return view_func(request, *args, **kwargs)
        
        # Si es ALUMNO o ESTUDIANTE, verificar que solo acceda a su propia información
        if cargo_usuario in ['ALUMNO', 'ESTUDIANTE']:
            # Obtener el ID del usuario actual
            id_usuario = request.session.get('idUsuario')
            
            try:
                # Obtener el alumno asociado al usuario
                alumno = Alumnos.objects.get(usuario_id=id_usuario)
                
                # Si hay un alumno_id en los kwargs, verificar que coincida con el alumno actual
                if 'alumno_id' in kwargs and int(kwargs['alumno_id']) != alumno.id:
                    messages.error(request, "No tiene permisos para acceder a esta información")
                    return redirect('/menu')
                
                # Añadir el alumno a los kwargs para que la vista pueda usarlo
                kwargs['alumno'] = alumno
                
                return view_func(request, *args, **kwargs)
            except Alumnos.DoesNotExist:
                messages.error(request, "No se encontró información de alumno asociada a su cuenta")
                return redirect('/menu')
        
        # Si no es ninguno de los roles anteriores, denegar acceso
        messages.error(request, "No tiene permisos para acceder a esta página")
        return redirect('/menu')
    
    return _wrapped_view

def alumno_data_only(view_func):
    """
    Decorador para asegurar que los alumnos solo vean su propia información.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario es un alumno
        if request.session.get('cargo') == 'ALUMNO':
            # Obtener el ID del alumno desde la sesión
            alumno_id = request.session.get('id_alumno')
            
            # Añadir el ID del alumno a los kwargs para filtrar en la vista
            kwargs['alumno_id'] = alumno_id
            
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def login_or_session_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if (user and user.is_authenticated) or request.session.get('nomUsuario'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Debe iniciar sesión para acceder a esta página")
        return redirect('/login')
    return _wrapped_view
