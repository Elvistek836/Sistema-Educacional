from django.shortcuts import render, redirect
from django.contrib import messages
from horarios.models import Alumnos, Padre, Apoderado
from django.http import HttpRequest, HttpResponse

def registrar_alumno(request: HttpRequest):
    """
    Vista para registrar un nuevo alumno con sus padres y apoderados (inlines)
    """
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    idUsuario = request.session.get("idUsuario")
    
    if not nomUsuario:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)
    
    if request.method == 'POST':
        try:
            # Crear el alumno
            from django.utils import timezone
            from django.db.models import Max
            max_matricula = Alumnos.objects.aggregate(Max('matricula')).get('matricula__max') or 0
            next_matricula = max_matricula + 1
            alumno = Alumnos(
                matricula=next_matricula,
                Administrativo_id=idUsuario,
                FechaHoraRegistroMatriculaEstudiante=timezone.now(),
                curso=request.POST.get('curso'),
                run=request.POST.get('run'),
                email=request.POST.get('email'),
                nombre=request.POST.get('nombre'),
                apellido_paterno=request.POST.get('apellido_paterno'),
                apellido_materno=request.POST.get('apellido_materno'),
                direccion=request.POST.get('direccion', ''),
                comuna=request.POST.get('comuna', ''),
                procedencia=request.POST.get('procedencia', ''),
                curso_repetido=request.POST.get('curso_repetido', 'NO APLICA'),
                con_quien_vive=request.POST.get('con_quien_vive', ''),
                enfermedad=request.POST.get('enfermedad', ''),
                prevision=request.POST.get('prevision', 'Ninguna'),
                letra_fonasa=request.POST.get('letra_fonasa', 'NO APLICA'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento') if request.POST.get('fecha_nacimiento') else None,
                edad=int(request.POST.get('edad')) if request.POST.get('edad') else None
            )
            alumno.save()
            
            # Procesar padres
            padre_count = 1
            while request.POST.get(f'padre_{padre_count}_nombre'):
                if request.POST.get(f'padre_{padre_count}_nombre').strip():
                    padre = Padre(
                        alumno=alumno,
                        es_madre=request.POST.get(f'padre_{padre_count}_es_madre') == 'on',
                        run=request.POST.get(f'padre_{padre_count}_run', ''),
                        nombre=request.POST.get(f'padre_{padre_count}_nombre', ''),
                        apellido_paterno=request.POST.get(f'padre_{padre_count}_apellido_paterno', ''),
                        apellido_materno=request.POST.get(f'padre_{padre_count}_apellido_materno', ''),
                        fono=request.POST.get(f'padre_{padre_count}_fono', ''),
                        escolaridad=request.POST.get(f'padre_{padre_count}_escolaridad', ''),
                        edad=int(request.POST.get(f'padre_{padre_count}_edad', 0)) if request.POST.get(f'padre_{padre_count}_edad') else None,
                        ocupacion=request.POST.get(f'padre_{padre_count}_ocupacion', ''),
                        religion=request.POST.get(f'padre_{padre_count}_religion', '')
                    )
                    padre.save()
                padre_count += 1
            
            # Procesar apoderados
            apoderado_count = 1
            while request.POST.get(f'apoderado_{apoderado_count}_nombre'):
                if request.POST.get(f'apoderado_{apoderado_count}_nombre').strip():
                    apoderado = Apoderado(
                        alumno=alumno,
                        run=request.POST.get(f'apoderado_{apoderado_count}_run', ''),
                        nombre=request.POST.get(f'apoderado_{apoderado_count}_nombre', ''),
                        apellido_paterno=request.POST.get(f'apoderado_{apoderado_count}_apellido_paterno', ''),
                        apellido_materno=request.POST.get(f'apoderado_{apoderado_count}_apellido_materno', ''),
                        fono=request.POST.get(f'apoderado_{apoderado_count}_fono', ''),
                        escolaridad=request.POST.get(f'apoderado_{apoderado_count}_escolaridad', ''),
                        edad=int(request.POST.get(f'apoderado_{apoderado_count}_edad', 0)) if request.POST.get(f'apoderado_{apoderado_count}_edad') else None,
                        ocupacion=request.POST.get(f'apoderado_{apoderado_count}_ocupacion', ''),
                        religion=request.POST.get(f'apoderado_{apoderado_count}_religion', '')
                    )
                    apoderado.save()
                apoderado_count += 1
            
            messages.success(request, f'Alumno {alumno.nombre} {alumno.apellido_paterno} registrado exitosamente.')
            return redirect('registrar_alumno')
            
        except Exception as e:
            messages.error(request, f'Error al registrar el alumno: {str(e)}')
            print(f"Error en registro de alumno: {str(e)}")
    
    from django.db.models import Max
    max_matricula = Alumnos.objects.aggregate(Max('matricula')).get('matricula__max') or 0
    context = {
        'nomUsuario': nomUsuario,
        'cargoUsuario': cargoUsuario,
        'cargo': cargoUsuario,
        'next_matricula': max_matricula + 1
    }
    return render(request, 'registrar_alumno.html', context)

def listar_padres(request: HttpRequest):
    """Vista para listar todos los padres/apoderados"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        padres = Padre.objects.select_related('alumno').filter(habilitado=True).order_by('apellido_paterno', 'apellido_materno', 'nombre')
        alumnos = Alumnos.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombre')
        
        context = {
            'padres': padres,
            'alumnos': alumnos,
            'total_padres': padres.count(),
            'total_madres': padres.filter(es_madre=True).count(),
            'total_padres_masculinos': padres.filter(es_madre=False).count(),
            'nomUsuario': request.session.get('nomUsuario'),
            'cargo': request.session.get('cargoUsuario'),
        }
        
        return render(request, 'listar_padres.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar la lista de padres: {str(e)}')
        return redirect('index')

def mostrar_registrar_padre(request: HttpRequest):
    """Vista para mostrar el formulario de registro de padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    
    try:
        alumnos = Alumnos.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombre')
        
        context = {
            'alumnos': alumnos,
            'nomUsuario': request.session.get('nomUsuario'),
            'cargoUsuario': request.session.get('cargoUsuario'),
            'cargo': request.session.get('cargoUsuario'),
        }
        
        return render(request, 'registrar_padre.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar el formulario: {str(e)}')
        return redirect('listar_padres')

def registrar_padre(request: HttpRequest):
    """Vista para procesar el registro de un nuevo padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        
        try:
            # Obtener datos del formulario
            alumno_id = request.POST.get('alumno')
            es_madre = request.POST.get('es_madre') == 'True'
            run = request.POST.get('run', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            apellido_paterno = request.POST.get('apellido_paterno', '').strip()
            apellido_materno = request.POST.get('apellido_materno', '').strip()
            fono = request.POST.get('fono', '').strip()
            escolaridad = request.POST.get('escolaridad', '').strip()
            ocupacion = request.POST.get('ocupacion', '').strip()
            edad = request.POST.get('edad', '').strip()
            religion = request.POST.get('religion', '').strip()
            
            # Validaciones
            if not alumno_id:
                messages.error(request, 'Debe seleccionar un alumno.')
                return redirect('mostrar_registrar_padre')
            
            if not run:
                messages.error(request, 'El RUN es obligatorio.')
                return redirect('mostrar_registrar_padre')
            
            if not nombre:
                messages.error(request, 'El nombre es obligatorio.')
                return redirect('mostrar_registrar_padre')
            
            if not apellido_paterno:
                messages.error(request, 'El apellido paterno es obligatorio.')
                return redirect('mostrar_registrar_padre')
            
            if edad and not edad.isdigit():
                messages.error(request, 'La edad debe ser un número válido.')
                return redirect('mostrar_registrar_padre')
            
            # Verificar que el alumno existe
            try:
                alumno = Alumnos.objects.get(pk=alumno_id)
            except Alumnos.DoesNotExist:
                messages.error(request, 'El alumno seleccionado no existe.')
                return redirect('mostrar_registrar_padre')
            
            # Verificar que no exista otro padre/madre del mismo tipo para este alumno
            if Padre.objects.filter(alumno=alumno, es_madre=es_madre).exists():
                tipo_padre = 'madre' if es_madre else 'padre'
                messages.error(request, f'Ya existe un {tipo_padre} registrado para este alumno.')
                return redirect('mostrar_registrar_padre')
            
            # Verificar que no exista otro padre con el mismo RUN
            if Padre.objects.filter(run=run).exists():
                messages.error(request, 'Ya existe un padre/apoderado con este RUN.')
                return redirect('mostrar_registrar_padre')
            
            # Crear el padre
            padre = Padre(
                alumno=alumno,
                es_madre=es_madre,
                run=run,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                fono=fono,
                escolaridad=escolaridad,
                ocupacion=ocupacion,
                edad=int(edad) if edad else None,
                religion=religion
            )
            
            padre.save()
            
            tipo_padre = 'madre' if es_madre else 'padre'
            messages.success(request, f'{tipo_padre.capitalize()} registrado exitosamente.')
            return redirect('listar_padres')
            
        except Exception as e:
            messages.error(request, f'Error al registrar el padre: {str(e)}')
            return redirect('mostrar_registrar_padre')
    
    return redirect('mostrar_registrar_padre')

def mostrar_modificar_padre(request: HttpRequest, id_padre: int):
    """Vista para mostrar el formulario de modificación de padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    
    try:
        padre = Padre.objects.get(id=id_padre)
        alumnos = Alumnos.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombre')
        
        nomUsuario = request.session.get('nomUsuario')
        cargoUsuario = request.session.get('cargoUsuario')
        
        context = {
            'padre': padre,
            'alumnos': alumnos,
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'cargo': cargoUsuario,
        }
        
        return render(request, 'modificar_padre.html', context)
        
    except Padre.DoesNotExist:
        messages.error(request, 'El padre especificado no existe.')
        return redirect('listar_padres')
    except Exception as e:
        messages.error(request, f'Error al cargar el formulario: {str(e)}')
        return redirect('listar_padres')

def modificar_padre(request: HttpRequest, id_padre: int):
    """Vista para procesar la modificación de un padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        
        try:
            padre = Padre.objects.get(id=id_padre)
            
            # Obtener datos del formulario
            alumno_id = request.POST.get('alumno')
            es_madre = request.POST.get('es_madre') == 'True'
            run = request.POST.get('run', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            apellido_paterno = request.POST.get('apellido_paterno', '').strip()
            apellido_materno = request.POST.get('apellido_materno', '').strip()
            fono = request.POST.get('fono', '').strip()
            escolaridad = request.POST.get('escolaridad', '').strip()
            ocupacion = request.POST.get('ocupacion', '').strip()
            edad = request.POST.get('edad', '').strip()
            religion = request.POST.get('religion', '').strip()
            
            # Validaciones
            # Si no viene 'alumno' en el POST, usar el actualmente asociado (fallback)
            if not alumno_id:
                alumno_id = str(padre.alumno.id) if getattr(padre, 'alumno', None) else None
            if not alumno_id:
                messages.error(request, 'Debe seleccionar un alumno.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            if not run:
                messages.error(request, 'El RUN es obligatorio.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            if not nombre:
                messages.error(request, 'El nombre es obligatorio.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            if not apellido_paterno:
                messages.error(request, 'El apellido paterno es obligatorio.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            if edad and not edad.isdigit():
                messages.error(request, 'La edad debe ser un número válido.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            # Verificar que el alumno existe
            try:
                alumno = Alumnos.objects.get(pk=alumno_id)
            except Alumnos.DoesNotExist:
                messages.error(request, 'El alumno seleccionado no existe.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            # Verificar que no exista otro padre/madre del mismo tipo para este alumno (excluyendo el actual)
            if Padre.objects.filter(alumno=alumno, es_madre=es_madre).exclude(id=id_padre).exists():
                tipo_padre = 'madre' if es_madre else 'padre'
                messages.error(request, f'Ya existe un {tipo_padre} registrado para este alumno.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            # Verificar que no exista otro padre con el mismo RUN (excluyendo el actual)
            if Padre.objects.filter(run=run).exclude(id=id_padre).exists():
                messages.error(request, 'Ya existe un padre/apoderado con este RUN.')
                return redirect('mostrar_modificar_padre', id_padre=id_padre)
            
            # Actualizar datos
            padre.alumno = alumno
            padre.es_madre = es_madre
            padre.run = run
            padre.nombre = nombre
            padre.apellido_paterno = apellido_paterno
            padre.apellido_materno = apellido_materno
            padre.fono = fono
            padre.escolaridad = escolaridad
            padre.ocupacion = ocupacion
            padre.edad = int(edad) if edad else None
            padre.religion = religion
            
            padre.save()
            
            tipo_padre = 'madre' if es_madre else 'padre'
            messages.success(request, f'{tipo_padre.capitalize()} modificado exitosamente.')
            return redirect('listar_padres')
            
        except Padre.DoesNotExist:
            messages.error(request, 'El padre especificado no existe.')
            return redirect('listar_padres')
        except Exception as e:
            messages.error(request, f'Error al modificar el padre: {str(e)}')
            return redirect('listar_padres')
    
    return redirect('listar_padres')

def eliminar_padre(request: HttpRequest, id_padre: int):
    """Vista para eliminar un padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        
        padre = Padre.objects.get(id=id_padre)
        tipo_padre = 'madre' if padre.es_madre else 'padre'
        padre.habilitado = False
        padre.save()

        messages.success(request, f'{tipo_padre.capitalize()} deshabilitado exitosamente.')
        return redirect('listar_padres')
        
    except Padre.DoesNotExist:
        messages.error(request, 'El padre especificado no existe.')
        return redirect('listar_padres')
    except Exception as e:
        messages.error(request, f'Error al eliminar el padre: {str(e)}')
        return redirect('listar_padres')

def listar_alumnos(request: HttpRequest):
    """Vista para listar alumnos con opción de exportar"""
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        alumnos = Alumnos.objects.all().order_by('matricula')
        
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'cargo': cargoUsuario,
            'alumnos': alumnos,
            'titulo': 'Lista de Alumnos'
        }
        
        return render(request, 'listar_alumnos.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

def exportar_alumnos_excel(request: HttpRequest):
    """Exportar lista de alumnos a Excel"""
    from django.http import HttpResponse
    import openpyxl
    from django.contrib.auth.models import User
    from django.db.models.fields.files import ImageFieldFile
    
    # Crear workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Matriculas de Alumnos'
    
    # Agregar encabezados del modelo principal (Alumnos)
    headers = [field.verbose_name for field in Alumnos._meta.fields if field.name != 'Administrativo' and field.name != 'Foto']
    
    # Agregar encabezados adicionales para inlines (Padres y Apoderados)
    headers += ['Padre o Madre', 'Run Padre', 'Nombre Padre', 'Apellido Paterno Padre', 'Apellido Materno Padre', 'Fono Padre', 'Escolaridad Padre', 'Edad Padre', 'Ocupacion Padre', 'Religion Padre', 'Run Apoderado', 'Nombre Apoderado', 'Apellido Paterno Apoderado', 'Apellido Materno Apoderado', 'Fono Apoderado', 'Escolaridad Apoderado', 'Edad Apoderado', 'Ocupacion Apoderado', 'Religion Apoderado']
    
    # Agregar encabezados a la hoja de Excel
    ws.append(headers)
    
    # Obtener todos los alumnos
    alumnos = Alumnos.objects.all()
    
    for obj in alumnos:
        # Datos del modelo principal (Alumnos)
        alumno_data = []
        for field in Alumnos._meta.fields:
            value = getattr(obj, field.name)
            if field.name != 'Administrativo' and field.name != 'Foto':
                # Si es la fecha, convertirla a string
                if field.name == 'FechaHoraRegistroMatriculaEstudiante':
                    value = str(value)
                elif isinstance(value, (User, ImageFieldFile)):
                    value = str(value)
                alumno_data.append(value)
        
        # Datos de inlines (Padres)
        padres_data = []
        for inline in obj.Padres.all():
            tipo_padre = 'Madre' if getattr(inline, 'es_madre', False) else 'Padre'
            run_padre = getattr(inline, 'run', '')
            nombre_padre = getattr(inline, 'nombre', '')
            apellidop_padre = getattr(inline, 'apellido_paterno', '')
            apellidom_padre = getattr(inline, 'apellido_materno', '')
            fono_padre = getattr(inline, 'fono', '')
            escolaridad_padre = getattr(inline, 'escolaridad', '')
            edad_padre = getattr(inline, 'edad', '')
            ocupacion_padre = getattr(inline, 'ocupacion', '')
            religion_padre = getattr(inline, 'religion', '')
            
            padres_data = [tipo_padre, run_padre, nombre_padre, apellidop_padre, apellidom_padre, fono_padre, escolaridad_padre, edad_padre, ocupacion_padre, religion_padre]
        
        # Datos de inlines (Apoderados)
        apoderados_data = []
        for inline in obj.Apoderados.all():
            run_apoderado = getattr(inline, 'run', '')
            nombre_apoderado = getattr(inline, 'nombre', '')
            apellidop_apoderado = getattr(inline, 'apellido_paterno', '')
            apellidom_apoderado = getattr(inline, 'apellido_materno', '')
            fono_apoderado = getattr(inline, 'fono', '')
            escolaridad_apoderado = getattr(inline, 'escolaridad', '')
            edad_apoderado = getattr(inline, 'edad', '')
            ocupacion_apoderado = getattr(inline, 'ocupacion', '')
            religion_apoderado = getattr(inline, 'religion', '')
            
            apoderados_data = [run_apoderado, nombre_apoderado, apellidop_apoderado, apellidom_apoderado, fono_apoderado, escolaridad_apoderado, edad_apoderado, ocupacion_apoderado, religion_apoderado]
        
        # Unir los datos de alumnos con padres y apoderados en una fila
        fila = alumno_data + padres_data + apoderados_data
        
        # Añadir la fila a la hoja de Excel
        ws.append(fila)
    
    # Preparar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment;filename=Matriculas_de_Alumnos.xlsx'
    
    # Guardar el archivo Excel en la respuesta
    wb.save(response)
    
    return response