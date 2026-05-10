from django.shortcuts import render, redirect
from django.contrib import messages
from horarios.models import Profesor, Actividades, Usuario
from django.http import HttpRequest
from horarios.decorators import role_required
from django.contrib.auth.models import User

@role_required(allowed_roles=['DIRECTOR', 'PROFESOR', 'ESTUDIANTE', 'ADMINISTRADOR'])
def listar_actividades(request: HttpRequest):
    """Vista para listar todas las actividades"""
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        actividades = Actividades.objects.all().order_by('-FechaHoraRegistro')
        if cargoUsuario=="PROFESOR":
            datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
            context = {
                'nomUsuario': nomUsuario,
                'cargo': cargoUsuario,
                'actividades': actividades,
                'datpro':datpro
            }
            return render(request, 'listar_actividades.html', context)
        else:
            context = {
                'nomUsuario': nomUsuario,
                'cargo': cargoUsuario,
                'actividades': actividades
                }
            return render(request, 'listar_actividades.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

def mostrar_registrar_actividad(request: HttpRequest):
    """Vista para mostrar el formulario de registro de actividades"""
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        if cargoUsuario=="PROFESOR":
            datpro=Profesor.objects.filter(email=nomUsuario.lower())
            context = {
                'nomUsuario': nomUsuario,
                'cargoUsuario': cargoUsuario,
                'titulo': 'Registrar Actividad',
                'datpro':datpro,
                'cargo':cargoUsuario
            }
            return render(request, 'registrar_actividad.html', context)
        else:
            context = {
                'nomUsuario': nomUsuario,
                'cargoUsuario': cargoUsuario,
                'titulo': 'Registrar Actividad',
                'cargo':cargoUsuario
            }
            return render(request, 'registrar_actividad.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

def registrar_actividad(request: HttpRequest):
    """Vista para procesar el registro de una nueva actividad"""
    
    if request.method == "POST":
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        
        if nomUsuario:
            try:
                usuario = Usuario.objects.filter(id=idUsuario).first()
                django_user = usuario.user if usuario else None
                actividad = Actividades(
                    Tipo=request.POST.get('tipo'),
                    Profesor=django_user,
                    Nombre=request.POST.get('nombre'),
                    FechaHoraPlanificada=request.POST.get('fecha_planificada'),
                    Observacion=request.POST.get('observacion'),
                    NumeroParticipantesActividad=request.POST.get('participantes', 0)
                )
                
                # Manejar archivos de fotos
                if 'foto1' in request.FILES:
                    actividad.Foto1 = request.FILES['foto1']
                if 'foto2' in request.FILES:
                    actividad.Foto2 = request.FILES['foto2']
                if 'foto3' in request.FILES:
                    actividad.Foto3 = request.FILES['foto3']
                
                actividad.save()
                
                messages.success(request, 'Actividad registrada correctamente!')
                return redirect('listar_actividades')
                
            except Exception as e:
                messages.error(request, f'Error al registrar la actividad: {str(e)}')
                return redirect('mostrar_registrar_actividad')
        else:
            datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
            return render(request, 'index.html', datos)
    else:
        # Redirigir a la página de mostrar formulario en lugar de a sí mismo
        return redirect('/mostrar_registrar_actividad')

def mostrar_modificar_actividad(request: HttpRequest, hash_id: str):
    """Vista para mostrar el formulario de modificación de actividad"""
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        try:
            id_actividad = Actividades.decode_hash(hash_id)
            actividad = Actividades.objects.get(id=id_actividad)
            
            context = {
                'nomUsuario': nomUsuario,
                'cargoUsuario': cargoUsuario,
                'actividad': actividad,
                'cargo': cargoUsuario,
                'titulo': 'Modificar Actividad'
                
            }
            
            return render(request, 'modificar_actividad.html', context)
            
        except Actividades.DoesNotExist:
            messages.error(request, 'Actividad no encontrada')
            return redirect('listar_actividades')
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

def modificar_actividad(request: HttpRequest, hash_id: str):
    """Vista para procesar la modificación de una actividad"""
    
    if request.method == "POST":
        nomUsuario = request.session.get("nomUsuario")
        
        if nomUsuario:
            try:
                id_actividad = Actividades.decode_hash(hash_id)
                actividad = Actividades.objects.get(id=id_actividad)
                
                actividad.Tipo = request.POST.get('tipo')
                actividad.Nombre = request.POST.get('nombre')
                actividad.FechaHoraPlanificada = request.POST.get('fecha_planificada')
                actividad.Observacion = request.POST.get('observacion')
                actividad.NumeroParticipantesActividad = request.POST.get('participantes', 0)
                
                # Manejar archivos de fotos
                if 'foto1' in request.FILES:
                    actividad.Foto1 = request.FILES['foto1']
                if 'foto2' in request.FILES:
                    actividad.Foto2 = request.FILES['foto2']
                if 'foto3' in request.FILES:
                    actividad.Foto3 = request.FILES['foto3']
                
                actividad.save()
                
                messages.success(request, 'Actividad modificada correctamente!')
                return redirect('listar_actividades')
                
            except Actividades.DoesNotExist:
                messages.error(request, 'Actividad no encontrada')
                return redirect('listar_actividades')
            except Exception as e:
                messages.error(request, f'Error al modificar la actividad: {str(e)}')
                return redirect('modificar_actividad', hash_id=hash_id)
        else:
            datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
            return render(request, 'index.html', datos)
    else:
        return redirect('modificar_actividad', hash_id=hash_id)

def eliminar_actividad(request: HttpRequest, hash_id: str):
    """Vista para eliminar una actividad"""
    
    nomUsuario = request.session.get("nomUsuario")
    
    if nomUsuario:
        try:
            id_actividad = Actividades.decode_hash(hash_id)
            actividad = Actividades.objects.get(id=id_actividad)
            actividad.delete()
            
            messages.success(request, 'Actividad eliminada correctamente!')
            
        except Actividades.DoesNotExist:
            messages.error(request, 'Actividad no encontrada')
        except Exception as e:
            messages.error(request, f'Error al eliminar la actividad: {str(e)}')
            
        return redirect('listar_actividades')
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)
