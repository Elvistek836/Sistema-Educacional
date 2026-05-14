from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from horarios.models import ConsejosProfesores
from django.contrib.auth.models import User
from horarios.decorators import role_required

@role_required(["ADMINISTRADOR", "DIRECTOR"])
def listar_consejos(request: HttpRequest):
    """Vista para listar todos los consejos de profesores"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    consejos = ConsejosProfesores.objects.all().order_by('FechaHoraPlanificadaConsejo')
    from django.utils import timezone
    now = timezone.localtime()
    hoy = now.date()
    consejos_total = consejos.count()
    consejos_hoy_count = ConsejosProfesores.objects.filter(FechaHoraPlanificadaConsejo__date=hoy, FechaHoraPlanificadaConsejo__gte=now).count()
    consejos_proximos_count = ConsejosProfesores.objects.filter(FechaHoraPlanificadaConsejo__date__gt=hoy).count()
    consejos_pasados_count = ConsejosProfesores.objects.filter(FechaHoraPlanificadaConsejo__lt=now).count()
    
    context = {
        'titulo': 'Gestión de Consejos de Profesores',
        'nomUsuario': request.session.get('nomUsuario'),
        'cargoUsuario': request.session.get('cargoUsuario'),
        'consejos': consejos,
        'cargo': request.session.get('cargoUsuario'),
        'consejos_total': consejos_total,
        'consejos_hoy_count': consejos_hoy_count,
        'consejos_proximos_count': consejos_proximos_count,
        'consejos_pasados_count': consejos_pasados_count,
    }
    return render(request, 'listar_consejos.html', context)

@role_required(["ADMINISTRADOR"])
def mostrar_registrar_consejo(request: HttpRequest):
    """Vista para mostrar el formulario de registro de consejo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    context = {
        'titulo': 'Registrar Nuevo Consejo de Profesores',
        'nomUsuario': request.session.get('nomUsuario'),
        'cargoUsuario': request.session.get('cargoUsuario'),
        'cargo': request.session.get('cargoUsuario'),
    }
    return render(request, 'registrar_consejo.html', context)

@role_required(["ADMINISTRADOR"])
def registrar_consejo(request: HttpRequest):
    """Vista para procesar el registro de un nuevo consejo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            fecha_planificada = request.POST.get('fecha_planificada')
            comentarios = request.POST.get('comentarios', '').strip()
            acuerdos = request.POST.get('acuerdos', '').strip()
            numero_profesores = request.POST.get('numero_profesores')
            
            # Validaciones
            if not fecha_planificada:
                messages.error(request, 'La fecha planificada es obligatoria.')
                return redirect('mostrar_registrar_consejo')
            
            if not comentarios:
                messages.error(request, 'Los comentarios son obligatorios.')
                return redirect('mostrar_registrar_consejo')
            
            if not acuerdos:
                messages.error(request, 'Los acuerdos son obligatorios.')
                return redirect('mostrar_registrar_consejo')
            
            if not numero_profesores or int(numero_profesores) <= 0:
                messages.error(request, 'El número de profesores debe ser mayor a cero.')
                return redirect('mostrar_registrar_consejo')
            
            # Validar fecha
            from datetime import datetime
            try:
                fecha_obj = datetime.strptime(fecha_planificada, '%Y-%m-%dT%H:%M')
            except ValueError:
                messages.error(request, 'Formato de fecha inválido.')
                return redirect('mostrar_registrar_consejo')
            
            # Obtener usuario actual de forma robusta
            id_auth = request.session.get('idAuthUser')
            django_user = User.objects.filter(id=id_auth).first()
            if not django_user:
                django_user = User.objects.filter(username__iexact=request.session.get('nomUsuario')).first()
            if not django_user:
                messages.error(request, 'No se pudo identificar al usuario autenticado.')
                return redirect('mostrar_registrar_consejo')
            
            # Crear nuevo consejo
            nuevo_consejo = ConsejosProfesores(
                Administrativo=django_user,
                FechaHoraPlanificadaConsejo=fecha_obj,
                ComentariosConsejo=comentarios,
                AcuerdosConsejo=acuerdos,
                NumeroProfesoresConsejo=int(numero_profesores)
            )
            
            # Manejar archivos
            if 'archivo1' in request.FILES:
                nuevo_consejo.Archivo1Consejo = request.FILES['archivo1']
            if 'archivo2' in request.FILES:
                nuevo_consejo.Archivo2Consejo = request.FILES['archivo2']
            if 'archivo3' in request.FILES:
                nuevo_consejo.Archivo3Consejo = request.FILES['archivo3']
            
            nuevo_consejo.save()
            messages.success(request, 'Consejo de profesores registrado exitosamente.')
            return redirect('listar_consejos')
            
        except Exception as e:
            messages.error(request, f'Error al registrar el consejo: {str(e)}')
            return redirect('mostrar_registrar_consejo')
    
    return redirect('mostrar_registrar_consejo')

@role_required(["ADMINISTRADOR"])
def mostrar_modificar_consejo(request: HttpRequest, id_consejo: int):
    """Vista para mostrar el formulario de modificación de consejo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        consejo = ConsejosProfesores.objects.get(idConsejo=id_consejo)
        
        context = {
            'titulo': 'Modificar Consejo de Profesores',
            'nomUsuario': request.session.get('nomUsuario'),
            'cargoUsuario': request.session.get('cargoUsuario'),
            'consejo': consejo,
            'cargo': request.session.get('cargoUsuario'),
        }
        return render(request, 'modificar_consejo.html', context)
    except ConsejosProfesores.DoesNotExist:
        messages.error(request, 'El consejo especificado no existe.')
        return redirect('listar_consejos')
    except Exception as e:
        messages.error(request, f'Error al cargar el consejo: {str(e)}')
        return redirect('listar_consejos')

@role_required(["ADMINISTRADOR"])
def modificar_consejo(request: HttpRequest, id_consejo: int):
    """Vista para procesar la modificación de un consejo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            consejo = ConsejosProfesores.objects.get(idConsejo=id_consejo)
            
            # Obtener datos del formulario
            fecha_planificada = request.POST.get('fecha_planificada')
            comentarios = request.POST.get('comentarios', '').strip()
            acuerdos = request.POST.get('acuerdos', '').strip()
            numero_profesores = request.POST.get('numero_profesores')
            
            # Validaciones
            if not fecha_planificada:
                messages.error(request, 'La fecha planificada es obligatoria.')
                return redirect('mostrar_modificar_consejo', id_consejo=id_consejo)
            
            if not comentarios:
                messages.error(request, 'Los comentarios son obligatorios.')
                return redirect('mostrar_modificar_consejo', id_consejo=id_consejo)
            
            if not acuerdos:
                messages.error(request, 'Los acuerdos son obligatorios.')
                return redirect('mostrar_modificar_consejo', id_consejo=id_consejo)
            
            if not numero_profesores or int(numero_profesores) <= 0:
                messages.error(request, 'El número de profesores debe ser mayor a cero.')
                return redirect('mostrar_modificar_consejo', id_consejo=id_consejo)
            
            # Validar fecha
            from datetime import datetime
            try:
                fecha_obj = datetime.strptime(fecha_planificada, '%Y-%m-%dT%H:%M')
            except ValueError:
                messages.error(request, 'Formato de fecha inválido.')
                return redirect('mostrar_modificar_consejo', id_consejo=id_consejo)
            
            # Actualizar datos
            consejo.FechaHoraPlanificadaConsejo = fecha_obj
            consejo.ComentariosConsejo = comentarios
            consejo.AcuerdosConsejo = acuerdos
            consejo.NumeroProfesoresConsejo = int(numero_profesores)
            
            # Manejar archivos
            if 'archivo1' in request.FILES:
                consejo.Archivo1Consejo = request.FILES['archivo1']
            if 'archivo2' in request.FILES:
                consejo.Archivo2Consejo = request.FILES['archivo2']
            if 'archivo3' in request.FILES:
                consejo.Archivo3Consejo = request.FILES['archivo3']
            
            consejo.save()
            messages.success(request, 'Consejo de profesores modificado exitosamente.')
            return redirect('listar_consejos')
            
        except ConsejosProfesores.DoesNotExist:
            messages.error(request, 'El consejo especificado no existe.')
            return redirect('listar_consejos')
        except Exception as e:
            messages.error(request, f'Error al modificar el consejo: {str(e)}')
            return redirect('listar_consejos')
    
    return redirect('listar_consejos')

@role_required(["ADMINISTRADOR"])
def eliminar_consejo(request: HttpRequest, id_consejo: int):
    """Vista para eliminar un consejo de profesores"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        consejo = ConsejosProfesores.objects.get(idConsejo=id_consejo)
        consejo.delete()
        messages.success(request, 'Consejo de profesores eliminado exitosamente.')
        return redirect('listar_consejos')
    except ConsejosProfesores.DoesNotExist:
        messages.error(request, 'El consejo especificado no existe.')
        return redirect('listar_consejos')
    except Exception as e:
        messages.error(request, f'Error al eliminar el consejo: {str(e)}')
        return redirect('listar_consejos')
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)