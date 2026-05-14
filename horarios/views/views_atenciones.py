from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from horarios.models import Profesor, Usuario, Atenciones, Alumnos
from horarios.decorators import role_required

@role_required(["ADMINISTRADOR", "PROFESOR"])
def listar_atenciones(request: HttpRequest):
    """Vista para listar todas las atenciones"""
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    atenciones = Atenciones.objects.all().order_by('-FechaHoraRegistro')
    if cargoUsuario=="PROFESOR":
        id_usuario = request.session.get('idUsuario')
        usuario = Usuario.objects.filter(id=id_usuario).first()
        django_user = usuario.user if usuario else None
        if django_user:
            atenciones = atenciones.filter(Profesional=django_user)
        email = (nomUsuario or '').lower()
        datpro = Profesor.objects.filter(email=email)
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'atenciones': atenciones,
            'titulo': 'Lista de Atenciones',
            'cargo':cargoUsuario,
            'datpro':datpro
        }
        return render(request, 'listar_atenciones.html', context)
    context = {
        'nomUsuario': nomUsuario,
        'cargoUsuario': cargoUsuario,
        'atenciones': atenciones,
        'cargo':cargoUsuario,
        'titulo': 'Lista de Atenciones'
    }
    return render(request, 'listar_atenciones.html', context)

@role_required(["ADMINISTRADOR", "PROFESOR"])
def mostrar_registrar_atencion(request: HttpRequest):
    """Vista para mostrar el formulario de registro de atenciones"""
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    alumnos = Alumnos.objects.all().order_by('nombre', 'apellido_paterno')
    if cargoUsuario=="PROFESOR":
        email = (nomUsuario or '').lower()
        datpro = Profesor.objects.filter(email=email)
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'alumnos': alumnos,
            'titulo': 'Registrar Atención',
            'cargo':cargoUsuario,
            'datpro':datpro
        }
        return render(request, 'registrar_atencion.html', context)
    context = {
        'nomUsuario': nomUsuario,
        'cargoUsuario': cargoUsuario,
        'alumnos': alumnos,
        'titulo': 'Registrar Atención',
        'cargo':cargoUsuario,
    }
    return render(request, 'registrar_atencion.html', context)

@role_required(["ADMINISTRADOR", "PROFESOR"])
def registrar_atencion(request: HttpRequest):
    """Vista para procesar el registro de una nueva atención"""
    
    if request.method == "POST":
        try:
            alumno = Alumnos.objects.get(pk=request.POST.get('alumno_id'))
            id_usuario = request.session.get('idUsuario')
            usuario = Usuario.objects.filter(id=id_usuario).first()
            django_user = usuario.user if usuario else None
            atencion = Atenciones(
                Tipo=request.POST.get('tipo'),
                Profesional=django_user,
                idMatricula=alumno,
                Motivo=request.POST.get('motivo'),
                Observaciones=request.POST.get('observacion')
            )
            atencion.save()
            messages.success(request, 'Atención registrada correctamente!')
            return redirect('listar_atenciones')
        except Alumnos.DoesNotExist:
            messages.error(request, 'Alumno no encontrado')
            return redirect('mostrar_registrar_atencion')
        except Exception as e:
            messages.error(request, f'Error al registrar la atención: {str(e)}')
            return redirect('mostrar_registrar_atencion')
    return redirect('mostrar_registrar_atencion')

@role_required(["ADMINISTRADOR", "PROFESOR"])
def mostrar_modificar_atencion(request: HttpRequest, hash_id):
    """Vista para mostrar el formulario de modificación de atención"""
    
    try:
        id_atencion = Atenciones.decode_hash(hash_id)
        atencion = Atenciones.objects.get(id=id_atencion)
        alumnos = Alumnos.objects.all().order_by('nombre', 'apellido_paterno')
        context = {
            'nomUsuario': request.session.get("nomUsuario") or (request.user.username if request.user.is_authenticated else None),
            'cargoUsuario': request.session.get("cargoUsuario"),
            'atencion': atencion,
            'alumnos': alumnos,
            'cargo': request.session.get("cargoUsuario"),
            'titulo': 'Modificar Atención'
        }
        return render(request, 'modificar_atencion.html', context)
    except Atenciones.DoesNotExist:
        messages.error(request, 'Atención no encontrada')
        return redirect('listar_atenciones')

@role_required(["ADMINISTRADOR", "PROFESOR"])
def modificar_atencion(request: HttpRequest, hash_id):
    """Vista para procesar la modificación de una atención"""
    
    
    if request.method == "POST":
        nomUsuario = request.session.get("nomUsuario")
        
        if nomUsuario:
            try:
                id_atencion = Atenciones.decode_hash(hash_id)
                atencion = Atenciones.objects.get(id=id_atencion)
                alumno = Alumnos.objects.get(pk=request.POST.get('alumno_id'))
                
                atencion.Tipo = request.POST.get('tipo')
                atencion.idMatricula = alumno
                atencion.Motivo = request.POST.get('motivo')
                atencion.Observaciones = request.POST.get('observacion')
                
                atencion.save()
                
                messages.success(request, 'Atención modificada correctamente!')
                return redirect('listar_atenciones')
                
            except Atenciones.DoesNotExist:
                messages.error(request, 'Atención no encontrada')
                return redirect('listar_atenciones')
            except Alumnos.DoesNotExist:
                messages.error(request, 'Alumno no encontrado')
                return redirect('modificar_atencion', hash_id=hash_id)
            except Exception as e:
                messages.error(request, f'Error al modificar la atención: {str(e)}')
                return redirect('modificar_atencion', hash_id=hash_id)
        else:
            datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
            return render(request, 'index.html', datos)
    else:
        return redirect('modificar_atencion', hash_id=hash_id)

@role_required(["ADMINISTRADOR", "PROFESOR"])
def eliminar_atencion(request: HttpRequest, hash_id):
    """Vista para eliminar una atención"""
    
    
    nomUsuario = request.session.get("nomUsuario")
    
    if nomUsuario:
        try:
            id_atencion = Atenciones.decode_hash(hash_id)
            atencion = Atenciones.objects.get(id=id_atencion)
            atencion.delete()
            
            messages.success(request, 'Atención eliminada correctamente!')
            
        except Atenciones.DoesNotExist:
            messages.error(request, 'Atención no encontrada')
        except Exception as e:
            messages.error(request, f'Error al eliminar la atención: {str(e)}')
            
        return redirect('listar_atenciones')
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)
