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

@role_required(["ADMINISTRADOR","DIRECTOR"])
def listar_insumos(request):
    """Vista para listar todos los insumos"""
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        insumos = Insumos.objects.all().order_by('NombreInsumo')
        
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'cargo': cargoUsuario,
            'insumos': insumos,
            'titulo': 'Lista de Insumos'
        }
        
        return render(request, 'listar_insumos.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

@role_required(["ADMINISTRADOR"])
def mostrar_registrar_insumo(request):
    """Vista para mostrar el formulario de registro de insumos"""
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'cargo': cargoUsuario,
            'titulo': 'Registrar Insumo'
        }
        
        return render(request, 'registrar_insumo.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

@role_required(["ADMINISTRADOR"])
def registrar_insumo(request):
    """Vista para procesar el registro de un nuevo insumo"""
    
    if request.method == "POST":
        nomUsuario = request.session.get("nomUsuario")
        
        if nomUsuario:
            try:
                # Verificar si ya existe un insumo con el mismo nombre
                nombre = request.POST.get('nombre')
                if Insumos.objects.filter(NombreInsumo=nombre).exists():
                    messages.error(request, 'Ya existe un insumo con ese nombre')
                    return redirect('mostrar_registrar_insumo')
                
                insumo = Insumos(
                    NombreInsumo=nombre,
                    DetalleInsumo=request.POST.get('descripcion') or '',
                    StockInsumo=int(request.POST.get('cantidad') or 0),
                    EstadoInsumo='BUENO'
                )
                
                # Manejar archivos de fotos
                if 'foto1' in request.FILES:
                    insumo.Foto1Insumo = request.FILES['foto1']
                if 'foto2' in request.FILES:
                    insumo.Foto2Insumo = request.FILES['foto2']
                if 'foto3' in request.FILES:
                    insumo.Foto3Insumo = request.FILES['foto3']

                insumo.save()
                
                messages.success(request, 'Insumo registrado correctamente!')
                return redirect('listar_insumos')
                
            except Exception as e:
                messages.error(request, f'Error al registrar el insumo: {str(e)}')
                return redirect('mostrar_registrar_insumo')
        else:
            datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
            return render(request, 'index.html', datos)
    else:
        return redirect('mostrar_registrar_insumo')

@role_required(["ADMINISTRADOR"])
def mostrar_modificar_insumo(request, id_insumo):
    """Vista para mostrar el formulario de modificación de insumo"""
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        try:
            insumo = Insumos.objects.get(IdInsumo=id_insumo)
            
            context = {
                'nomUsuario': nomUsuario,
                'cargoUsuario': cargoUsuario,
                'cargo': cargoUsuario,
                'insumo': insumo,
                'titulo': 'Modificar Insumo'
            }
            
            return render(request, 'modificar_insumo.html', context)
            
        except Insumos.DoesNotExist:
            messages.error(request, 'Insumo no encontrado')
            return redirect('listar_insumos')
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

@role_required(["ADMINISTRADOR"])
def modificar_insumo(request):
    """Vista para procesar la modificación de un insumo"""
    
    if request.method == "POST":
        nomUsuario = request.session.get("nomUsuario")
        
        if nomUsuario:
            try:
                id_insumo = request.POST.get('id_insumo')
                insumo = Insumos.objects.get(IdInsumo=id_insumo)
                
                # Verificar si ya existe otro insumo con el mismo nombre
                nombre = request.POST.get('nombre')
                if Insumos.objects.filter(NombreInsumo=nombre).exclude(IdInsumo=id_insumo).exists():
                    messages.error(request, 'Ya existe otro insumo con ese nombre')
                    return redirect('mostrar_modificar_insumo', id_insumo=id_insumo)
                
                insumo.NombreInsumo = nombre
                insumo.DetalleInsumo = request.POST.get('descripcion') or ''
                insumo.StockInsumo = int(request.POST.get('cantidad') or 0)

                # Manejar actualización de archivos de fotos
                if 'foto1' in request.FILES:
                    insumo.Foto1Insumo = request.FILES['foto1']
                if 'foto2' in request.FILES:
                    insumo.Foto2Insumo = request.FILES['foto2']
                if 'foto3' in request.FILES:
                    insumo.Foto3Insumo = request.FILES['foto3']

                insumo.save()
                
                messages.success(request, 'Insumo modificado correctamente!')
                return redirect('listar_insumos')
                
            except Insumos.DoesNotExist:
                messages.error(request, 'Insumo no encontrado')
                return redirect('listar_insumos')
            except Exception as e:
                messages.error(request, f'Error al modificar el insumo: {str(e)}')
                return redirect('mostrar_modificar_insumo', id_insumo=id_insumo)
        else:
            datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
            return render(request, 'index.html', datos)
    else:
        return redirect('listar_insumos')

@role_required(["ADMINISTRADOR"])
def eliminar_insumo(request, id_insumo):
    """Vista para eliminar un insumo"""
    
    nomUsuario = request.session.get("nomUsuario")
    
    if nomUsuario:
        try:
            insumo = Insumos.objects.get(IdInsumo=id_insumo)
            insumo.delete()
            
            messages.success(request, 'Insumo eliminado correctamente!')
            
        except Insumos.DoesNotExist:
            messages.error(request, 'Insumo no encontrado')
        except Exception as e:
            messages.error(request, f'Error al eliminar el insumo: {str(e)}')
        return redirect('listar_insumos')
