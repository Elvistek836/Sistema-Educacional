from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from horarios.models import Profesor, Asignatura, Curso, AsignaturasProfesor, DisponibilidadProfesor, Horario, Usuario, Historial, Alumnos, Padre, Apoderado, Impresiones, Insumos, Prestamos, ConsejosProfesores, CURSOS_CHOICE, ESTADOIMPRESION_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from horarios.decorators import role_required, profesor_data_only, alumno_data_only, login_or_session_required

@login_or_session_required
def listar_impresiones(request):
    """Vista para listar todas las impresiones"""
    try:
        nomUsuario = request.session.get('nomUsuario')
        cargo = request.session.get('cargoUsuario')
        es_privilegiado = cargo in ["ADMINISTRADOR", "UTP"]
        impresiones = Impresiones.objects.filter(habilitado=True).order_by('-FechaHoraRegistroImpresion')
        if cargo == "DIRECTOR":
            es_privilegiado = True
            context = {
                'titulo': 'Gestión de Impresiones',
                'nomUsuario': request.session.get('nomUsuario'),
                'cargoUsuario': cargo,
                'cargo': cargo,
                'impresiones': impresiones,
                'es_privilegiado': es_privilegiado,
            }
        if not es_privilegiado:
            id_usuario = request.session.get('idUsuario')
            usuario = Usuario.objects.filter(id=id_usuario).first()
            django_user = usuario.user if usuario else None
            if django_user:
                impresiones = impresiones.filter(ProfesorImpresion=django_user)
            else:
                impresiones = impresiones.none()
        if cargo == "PROFESOR":
            datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
            context = {
                'titulo': 'Gestión de Impresiones',
                'nomUsuario': request.session.get('nomUsuario'),
                'cargoUsuario': cargo,
                'impresiones': impresiones,
                'es_privilegiado': es_privilegiado,
                'datpro': datpro,
                'cargo': cargo,
            }
        else:
            context = {
                'titulo': 'Gestión de Impresiones',
                'nomUsuario': request.session.get('nomUsuario'),
                'cargoUsuario': cargo,
                'cargo': cargo,
                'impresiones': impresiones,
                'es_privilegiado': es_privilegiado,
            }
        return render(request, 'listar_impresiones.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar las impresiones: {str(e)}')
        return redirect('/menu')

@login_or_session_required
def mostrar_registrar_impresion(request):
    """Vista para mostrar el formulario de registro de impresiones"""
    try:
        context = {
            'titulo': 'Registrar Nueva Impresión',
            'nomUsuario': request.session.get('nomUsuario'),
            'cargoUsuario': request.session.get('cargoUsuario'),
            'cursos': CURSOS_CHOICE,
            'cargo': request.session.get('cargoUsuario'),
        }
        
        return render(request, 'registrar_impresion.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar el formulario: {str(e)}')
        return redirect('listar_impresiones')

@login_or_session_required
def registrar_impresion(request):
    """Vista para procesar el registro de una nueva impresión"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            fecha_utilizacion = request.POST.get('fecha_utilizacion')
            curso = request.POST.get('curso')
            asignatura = request.POST.get('asignatura', '').strip()
            observacion = request.POST.get('observacion', '').strip()
            archivo1 = request.FILES.get('archivo1')
            archivo2 = request.FILES.get('archivo2')
            archivo3 = request.FILES.get('archivo3')
            
            # Validaciones
            if not fecha_utilizacion:
                messages.error(request, 'La fecha y hora de utilización es obligatoria.')
                return redirect('mostrar_registrar_impresion')
            
            if not curso:
                messages.error(request, 'El curso es obligatorio.')
                return redirect('mostrar_registrar_impresion')
            
            if not asignatura:
                messages.error(request, 'La asignatura es obligatoria.')
                return redirect('mostrar_registrar_impresion')
            
            if not observacion:
                messages.error(request, 'La observación es obligatoria.')
                return redirect('mostrar_registrar_impresion')
            
            # Validar que al menos un archivo sea proporcionado
            if not any([archivo1, archivo2, archivo3]):
                messages.error(request, 'Debe adjuntar al menos un archivo.')
                return redirect('mostrar_registrar_impresion')
            
            # Validar formato de fecha
            try:
                fecha_utilizacion_obj = datetime.strptime(fecha_utilizacion, '%Y-%m-%dT%H:%M')
            except ValueError:
                messages.error(request, 'Formato de fecha inválido.')
                return redirect('mostrar_registrar_impresion')
            
            if timezone.is_naive(fecha_utilizacion_obj):
                fecha_utilizacion_obj = timezone.make_aware(fecha_utilizacion_obj, timezone.get_current_timezone())
            fecha_limite = timezone.now() - timedelta(days=7)
            if fecha_utilizacion_obj < fecha_limite:
                messages.error(request, 'No se puede registrar una impresión con fecha anterior a 7 días.')
                return redirect('mostrar_registrar_impresion')
            
            # Crear la nueva impresión
            id_usuario = request.session.get('idUsuario')
            usuario = Usuario.objects.filter(id=id_usuario).first()
            django_user = usuario.user if usuario else None
            nueva_impresion = Impresiones(
                ProfesorImpresion=django_user,
                FechaHoraUtilizacionImpresion=fecha_utilizacion_obj,
                CursoImpresion=curso,
                AsignaturaImpresion=asignatura,
                ObservacionImpresion=observacion,
                EstadoImpresion='PENDIENTE'
            )
            
            # Asignar archivos si existen
            if archivo1:
                nueva_impresion.Archivo1Impresion = archivo1
            if archivo2:
                nueva_impresion.Archivo2Impresion = archivo2
            if archivo3:
                nueva_impresion.Archivo3Impresion = archivo3
            
            nueva_impresion.save()
            
            messages.success(request, 'Impresión registrada exitosamente.')
            return redirect('listar_impresiones')
            
        except Exception as e:
            messages.error(request, f'Error al registrar la impresión: {str(e)}')
            return redirect('mostrar_registrar_impresion')
    
    return redirect('mostrar_registrar_impresion')

@login_or_session_required
def mostrar_modificar_impresion(request, id_impresion):
    """Vista para mostrar el formulario de modificación de impresiones"""
    try:
        impresion = get_object_or_404(Impresiones, idImpresion=id_impresion)
        cargo = request.session.get('cargoUsuario')
        id_usuario = request.session.get('idUsuario')
        usuario = Usuario.objects.filter(id=id_usuario).first()
        django_user = usuario.user if usuario else None
        if not (cargo in ["ADMINISTRADOR", "UTP"] or (django_user and impresion.ProfesorImpresion_id == django_user.id)):
            messages.error(request, 'No tiene permisos para modificar esta impresión.')
            return redirect('listar_impresiones')
        
        context = {
            'titulo': 'Modificar Impresión',
            'nomUsuario': request.session.get('nomUsuario'),
            'cargoUsuario': request.session.get('cargoUsuario'),
            'cargo': request.session.get('cargoUsuario'),
            'impresion': impresion,
            'cursos': CURSOS_CHOICE,
            'estados': ESTADOIMPRESION_CHOICES,
            'today': timezone.now().date(),
        }
        
        return render(request, 'modificar_impresion.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar la impresión: {str(e)}')
        return redirect('listar_impresiones')

@login_or_session_required
def modificar_impresion(request, id_impresion):
    """Vista para procesar la modificación de una impresión"""
    if request.method == 'POST':
        try:
            impresion = get_object_or_404(Impresiones, idImpresion=id_impresion)
            cargo = request.session.get('cargoUsuario')
            id_usuario = request.session.get('idUsuario')
            usuario = Usuario.objects.filter(id=id_usuario).first()
            django_user = usuario.user if usuario else None
            if not (cargo in ["ADMINISTRADOR", "UTP"] or (django_user and impresion.ProfesorImpresion_id == django_user.id)):
                messages.error(request, 'No tiene permisos para modificar esta impresión.')
                return redirect('listar_impresiones')
            
            # Obtener datos del formulario
            fecha_utilizacion = request.POST.get('fecha_utilizacion')
            curso = request.POST.get('curso')
            asignatura = request.POST.get('asignatura', '').strip()
            observacion = request.POST.get('observacion', '').strip()
            estado = request.POST.get('estado')
            archivo1 = request.FILES.get('archivo1')
            archivo2 = request.FILES.get('archivo2')
            archivo3 = request.FILES.get('archivo3')
            
            # Checkboxes para eliminar archivos
            eliminar_archivo1 = request.POST.get('eliminar_archivo1')
            eliminar_archivo2 = request.POST.get('eliminar_archivo2')
            eliminar_archivo3 = request.POST.get('eliminar_archivo3')
            
            # Validaciones
            if not fecha_utilizacion:
                messages.error(request, 'La fecha y hora de utilización es obligatoria.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            if not curso:
                messages.error(request, 'El curso es obligatorio.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            if not asignatura:
                messages.error(request, 'La asignatura es obligatoria.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            if not observacion:
                messages.error(request, 'La observación es obligatoria.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            if not estado:
                messages.error(request, 'El estado es obligatorio.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            # Validar formato de fecha
            try:
                fecha_utilizacion_obj = datetime.strptime(fecha_utilizacion, '%Y-%m-%dT%H:%M')
            except ValueError:
                messages.error(request, 'Formato de fecha inválido.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            if timezone.is_naive(fecha_utilizacion_obj):
                fecha_utilizacion_obj = timezone.make_aware(fecha_utilizacion_obj, timezone.get_current_timezone())
            impresion.FechaHoraUtilizacionImpresion = fecha_utilizacion_obj
            impresion.CursoImpresion = curso
            impresion.AsignaturaImpresion = asignatura
            impresion.ObservacionImpresion = observacion
            impresion.EstadoImpresion = estado
            
            # Manejar archivos
            if archivo1:
                impresion.Archivo1Impresion = archivo1
            elif eliminar_archivo1:
                impresion.Archivo1Impresion = None
            
            if archivo2:
                impresion.Archivo2Impresion = archivo2
            elif eliminar_archivo2:
                impresion.Archivo2Impresion = None
            
            if archivo3:
                impresion.Archivo3Impresion = archivo3
            elif eliminar_archivo3:
                impresion.Archivo3Impresion = None
            
            # Validar que al menos un archivo permanezca
            if not any([impresion.Archivo1Impresion, impresion.Archivo2Impresion, impresion.Archivo3Impresion]):
                messages.error(request, 'Debe mantener al menos un archivo adjunto.')
                return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
            
            impresion.save()
            
            messages.success(request, 'Impresión modificada exitosamente.')
            return redirect('listar_impresiones')
            
        except Exception as e:
            messages.error(request, f'Error al modificar la impresión: {str(e)}')
            return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)
    
    return redirect('mostrar_modificar_impresion', id_impresion=id_impresion)

@login_or_session_required
def eliminar_impresion(request, id_impresion):
    """Vista para eliminar una impresión"""
    try:
        impresion = get_object_or_404(Impresiones, idImpresion=id_impresion)
        cargo = request.session.get('cargoUsuario')
        id_usuario = request.session.get('idUsuario')
        usuario = Usuario.objects.filter(id=id_usuario).first()
        django_user = usuario.user if usuario else None
        if not (cargo in ["ADMINISTRADOR", "UTP"] or (django_user and impresion.ProfesorImpresion_id == django_user.id)):
            messages.error(request, 'No tiene permisos para eliminar esta impresión.')
            return redirect('listar_impresiones')
        
        # Eliminar archivos físicos si existen
        try:
            if impresion.Archivo1Impresion and impresion.Archivo1Impresion.name != 'images/impresiones/sinimagen.png':
                impresion.Archivo1Impresion.delete(save=False)
            if impresion.Archivo2Impresion and impresion.Archivo2Impresion.name != 'images/impresiones/sinimagen.png':
                impresion.Archivo2Impresion.delete(save=False)
            if impresion.Archivo3Impresion and impresion.Archivo3Impresion.name != 'images/impresiones/sinimagen.png':
                impresion.Archivo3Impresion.delete(save=False)
        except Exception as e:
            # Si hay error eliminando archivos, continuar con la eliminación del registro
            pass
        
        # Eliminar la impresión
        impresion.delete()
        
        messages.success(request, 'Impresión eliminada exitosamente.')
        return redirect('listar_impresiones')
        
    except Exception as e:
        messages.error(request, f'Error al eliminar la impresión: {str(e)}')
        return redirect('listar_impresiones')
