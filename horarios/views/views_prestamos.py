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

@role_required(["ADMINISTRADOR", "DIRECTOR"])
def listar_prestamos(request):
    """Lista todos los préstamos registrados"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    

    prestamos = Prestamos.objects.all().order_by('-FechaHoraRegistroPrestamo')
    
    # Verificar préstamos vencidos
    from django.utils import timezone
    hoy = timezone.now()
    
    for p in prestamos:
        # Verificar vencimiento si está SIN DEVOLVER y tiene fecha de devolución esperada
        if p.EstadoPrestamo == 'SIN DEVOLVER' and p.FechaHoraDevolucionPrestamo:
            if p.FechaHoraDevolucionPrestamo < hoy:
                p.EstadoPrestamo = 'VENCIDO'
                p.save()
                
        # Limpiar detalle para mostrar solo el mensaje legible
        import re
        p.detalle_limpio = re.sub(r'\[INSUMO_ID:\d+\]\s*\[CANT:\d+\]\s*', '', p.DetallePrestamo)
    
    activos_count = prestamos.filter(EstadoPrestamo='SIN DEVOLVER').count()
    vencidos_count = prestamos.filter(EstadoPrestamo='VENCIDO').count()
    devueltos_count = prestamos.filter(EstadoPrestamo='DEVUELTO').count()
    
    context = {
        'titulo': 'Gestión de Préstamos',
        'prestamos': prestamos,
        'prestamos_activos_count': activos_count,
        'prestamos_vencidos_count': vencidos_count,
        'prestamos_devueltos_count': devueltos_count,
        'nomUsuario': request.session.get('nomUsuario'),
        'cargoUsuario': request.session.get('cargoUsuario'),
        'cargo': request.session.get('cargoUsuario'),
    }
    return render(request, 'listar_prestamos.html', context)

@role_required(["ADMINISTRADOR", "UTP", "SECRETARIA", "DIRECTOR"])
def mostrar_registrar_prestamo(request):
    """Muestra el formulario para registrar un nuevo préstamo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        # Obtener insumos disponibles (con stock > 0)
        insumos_disponibles = Insumos.objects.filter(StockInsumo__gt=0).order_by('NombreInsumo')
        
        context = {
            'titulo': 'Registrar Nuevo Préstamo',
            'insumos': insumos_disponibles,
            'nomUsuario': request.session.get('nomUsuario'),
            'cargoUsuario': request.session.get('cargoUsuario'),
            'cargo': request.session.get('cargoUsuario'),
        }
        return render(request, 'registrar_prestamo.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar el formulario: {str(e)}')
        return redirect('listar_prestamos')

@role_required(["ADMINISTRADOR", "UTP", "SECRETARIA"])
def registrar_prestamo(request):
    """Procesa el registro de un nuevo préstamo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            id_insumo = request.POST.get('insumo')
            solicitante = request.POST.get('solicitante', '').strip()
            cantidad_str = request.POST.get('cantidad_prestada', '').strip()
            fecha_prestamo = request.POST.get('fecha_prestamo')
            fecha_devolucion_esperada = request.POST.get('fecha_devolucion_esperada')
            observaciones = request.POST.get('observaciones', '').strip()

            if not all([id_insumo, solicitante, cantidad_str, fecha_prestamo]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('mostrar_registrar_prestamo')

            try:
                cantidad_prestada = int(cantidad_str)
            except (TypeError, ValueError):
                messages.error(request, 'La cantidad debe ser un número válido.')
                return redirect('mostrar_registrar_prestamo')

            if cantidad_prestada <= 0:
                messages.error(request, 'La cantidad debe ser mayor a cero.')
                return redirect('mostrar_registrar_prestamo')

            insumo = Insumos.objects.get(IdInsumo=id_insumo)
            if insumo.StockInsumo < cantidad_prestada:
                messages.error(request, f'Stock insuficiente. Disponible: {insumo.StockInsumo}')
                return redirect('mostrar_registrar_prestamo')

            admin_user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
            if not admin_user:
                id_usuario = request.session.get('idUsuario')
                usuario_obj = None
                if id_usuario:
                    usuario_obj = Usuario.objects.filter(id=id_usuario).select_related('user').first()
                if not usuario_obj:
                    nom_usuario = request.session.get('nomUsuario')
                    usuario_obj = Usuario.objects.filter(nombre__iexact=nom_usuario).select_related('user').first()
                admin_user = usuario_obj.user if usuario_obj else None
            if not admin_user:
                messages.error(request, 'No se pudo determinar el usuario administrativo.')
                return redirect('mostrar_registrar_prestamo')

            detalle = f"[INSUMO_ID:{insumo.IdInsumo}] [CANT:{cantidad_prestada}] Prestamo de {insumo.NombreInsumo} x {cantidad_prestada} para {solicitante}. {observaciones}".strip()
            prestamo = Prestamos(
                Administrativo=admin_user,
                DetallePrestamo=detalle,
                EstadoPrestamo='SIN DEVOLVER'
            )

            if fecha_devolucion_esperada:
                try:
                    from datetime import datetime as _dt, time as _time
                    from django.utils.timezone import make_aware
                    fecha_dev = make_aware(_dt.combine(_dt.strptime(fecha_devolucion_esperada, '%Y-%m-%d').date(), _time.min))
                    prestamo.FechaHoraDevolucionPrestamo = fecha_dev
                except Exception:
                    pass

            prestamo.save()

            insumo.StockInsumo -= cantidad_prestada
            insumo.save()

            messages.success(request, f'Préstamo registrado exitosamente. ID: {prestamo.pk}')
            return redirect('listar_prestamos')

        except Insumos.DoesNotExist:
            messages.error(request, 'El insumo seleccionado no existe.')
            return redirect('mostrar_registrar_prestamo')
        except Exception as e:
            messages.error(request, f'Error al registrar el préstamo: {str(e)}')
            return redirect('mostrar_registrar_prestamo')
    
    return redirect('mostrar_registrar_prestamo')

@role_required(["ADMINISTRADOR", "UTP", "SECRETARIA", "DIRECTOR"])
def mostrar_modificar_prestamo(request, id_prestamo):
    """Muestra el formulario para modificar un préstamo existente"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        prestamo = Prestamos.objects.get(pk=id_prestamo)
        insumos_disponibles = Insumos.objects.all().order_by('NombreInsumo')
        
        context = {
            'titulo': 'Modificar Préstamo',
            'prestamo': prestamo,
            'insumos': insumos_disponibles,
            'nomUsuario': request.session.get('nomUsuario'),
            'cargoUsuario': request.session.get('cargoUsuario'),
            'cargo': request.session.get('cargoUsuario'),
        }
        return render(request, 'modificar_prestamo.html', context)
    except Prestamos.DoesNotExist:
        messages.error(request, 'El préstamo no existe.')
        return redirect('listar_prestamos')
    except Exception as e:
        messages.error(request, f'Error al cargar el préstamo: {str(e)}')
        return redirect('listar_prestamos')

@role_required(["ADMINISTRADOR", "UTP", "SECRETARIA"])
def modificar_prestamo(request):
    """Procesa la modificación de un préstamo"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            id_prestamo = request.POST.get('id_prestamo')
            estado = request.POST.get('estado')
            observaciones = request.POST.get('observaciones', '').strip()

            # Obtener el préstamo
            prestamo = Prestamos.objects.get(pk=id_prestamo)
            estado_anterior = prestamo.EstadoPrestamo

            # Actualizar campos
            if estado:
                prestamo.EstadoPrestamo = estado
                
                # Si el estado es VENCIDO, asegurarse que siga vencido si la fecha ya pasó
                if estado == 'SIN DEVOLVER' and prestamo.FechaHoraDevolucionPrestamo:
                    from django.utils import timezone
                    if prestamo.FechaHoraDevolucionPrestamo < timezone.now():
                        prestamo.EstadoPrestamo = 'VENCIDO'

            if observaciones:
                prestamo.DetallePrestamo = f"{prestamo.DetallePrestamo} | {observaciones}"[:500]

            # Fecha devolución real
            fecha_devolucion_real = request.POST.get('fecha_devolucion_real')
            if fecha_devolucion_real:
                try:
                    from datetime import datetime as _dt, time as _time
                    from django.utils.timezone import make_aware
                    fecha_dev = make_aware(_dt.combine(_dt.strptime(fecha_devolucion_real, '%Y-%m-%d').date(), _time.min))
                    
                    # Si estamos cambiando la fecha de devolución esperada (cuando aún no se devuelve)
                    # O si estamos registrando la fecha real de devolución
                    prestamo.FechaHoraDevolucionPrestamo = fecha_dev
                    
                    # Re-verificar vencimiento con la nueva fecha
                    if prestamo.EstadoPrestamo in ['SIN DEVOLVER', 'VENCIDO']:
                        from django.utils import timezone
                        if fecha_dev < timezone.now():
                            prestamo.EstadoPrestamo = 'VENCIDO'
                        else:
                            prestamo.EstadoPrestamo = 'SIN DEVOLVER'
                            
                except Exception:
                    pass

            # Restaurar stock cuando se marca como DEVUELTO por primera vez
            if estado and estado == 'DEVUELTO' and estado_anterior != 'DEVUELTO':
                import re
                insumo_id = None
                cantidad = None
                m = re.search(r"\[INSUMO_ID:(\d+)\]\s*\[CANT:(\d+)\]", prestamo.DetallePrestamo)
                if m:
                    insumo_id = int(m.group(1))
                    cantidad = int(m.group(2))
                else:
                    m2 = re.search(r"Prestamo de\s+(.+?)\s+x\s+(\d+)", prestamo.DetallePrestamo)
                    if m2:
                        nombre_insumo = m2.group(1).strip()
                        cantidad = int(m2.group(2))
                        try:
                            insumo_obj = Insumos.objects.filter(NombreInsumo=nombre_insumo).first()
                            if insumo_obj:
                                insumo_obj.StockInsumo += cantidad
                                insumo_obj.save()
                        except Exception:
                            pass
                if insumo_id and cantidad is not None:
                    try:
                        insumo_obj = Insumos.objects.get(IdInsumo=insumo_id)
                        insumo_obj.StockInsumo += cantidad
                        insumo_obj.save()
                    except Insumos.DoesNotExist:
                        pass

            prestamo.save()

            messages.success(request, 'Préstamo modificado exitosamente.')
            return redirect('listar_prestamos')
            
        except Prestamos.DoesNotExist:
            messages.error(request, 'El préstamo no existe.')
            return redirect('listar_prestamos')
        except ValueError:
            messages.error(request, 'La cantidad devuelta debe ser un número válido.')
            return redirect('mostrar_modificar_prestamo', id_prestamo=request.POST.get('id_prestamo'))
        except Exception as e:
            messages.error(request, f'Error al modificar el préstamo: {str(e)}')
            return redirect('listar_prestamos')
    
    return redirect('listar_prestamos')

@role_required(["ADMINISTRADOR", "UTP"])
def eliminar_prestamo(request, id_prestamo):
    """Elimina un préstamo (solo si no se ha devuelto nada)"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        prestamo = Prestamos.objects.get(pk=id_prestamo)
        # Restaurar stock solo si el préstamo estaba SIN DEVOLVER
        if prestamo.EstadoPrestamo == 'SIN DEVOLVER':
            import re
            insumo_id = None
            cantidad = None
            m = re.search(r"\[INSUMO_ID:(\d+)\]\s*\[CANT:(\d+)\]", prestamo.DetallePrestamo)
            if m:
                insumo_id = int(m.group(1))
                cantidad = int(m.group(2))
            else:
                m2 = re.search(r"Prestamo de\s+(.+?)\s+x\s+(\d+)", prestamo.DetallePrestamo)
                if m2:
                    nombre_insumo = m2.group(1).strip()
                    cantidad = int(m2.group(2))
                    try:
                        insumo_obj = Insumos.objects.filter(NombreInsumo=nombre_insumo).first()
                        if insumo_obj:
                            insumo_obj.StockInsumo += cantidad
                            insumo_obj.save()
                    except Exception:
                        pass
            if insumo_id and cantidad is not None:
                try:
                    insumo_obj = Insumos.objects.get(IdInsumo=insumo_id)
                    insumo_obj.StockInsumo += cantidad
                    insumo_obj.save()
                except Insumos.DoesNotExist:
                    pass

        prestamo.delete()
        messages.success(request, 'Préstamo eliminado exitosamente.')
        return redirect('listar_prestamos')
        
    except Prestamos.DoesNotExist:
        messages.error(request, 'El préstamo no existe.')
        return redirect('listar_prestamos')
    except Exception as e:
        messages.error(request, f'Error al eliminar el préstamo: {str(e)}')
        return redirect('listar_prestamos')
