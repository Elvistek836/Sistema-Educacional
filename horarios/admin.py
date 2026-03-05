from typing import Any
from django.db.models.fields.files import ImageFieldFile
import os
import io
from django.contrib import admin
from django.utils.timezone import is_aware, make_naive
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
import openpyxl
from reportlab.pdfgen import canvas
from openpyxl.drawing.image import Image
from openpyxl.utils import datetime
from django.http import HttpResponse
from django.db.models.fields.related import ForeignKey
from zipfile import ZipFile
from django.forms.models import ModelChoiceField
from django.urls import path
from django.shortcuts import render
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import (
    Profesor, Curso, Asignatura, AsignaturasProfesor,
    DisponibilidadProfesor, Horario, Usuario,
    Historial, Alumnos, Apoderado, Padre, Actividades,
    Atenciones, Insumos, Prestamos, Certificados,
    ConsejosProfesores, Impresiones
)
from .forms import (AlumnoForm, HorarioForm, DisponibilidadProfesorForm, AsignaturasProfesorForm,
                    AsignaturaForm, CursoForm, ProfesorForm, ActividadesForm, PrestamosForm, ImpresionesForm, ConsejosProfesoresForm, AtencionesForm, InsumosForm, CertificadosForm, ApoderadoForm, PadreForm)

#----------------------------------------------------
# DESACTIVAR LAS ACCIONES RECIENTES

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['has_permission'] = False  # Desactivar panel de acciones recientes
        return context

admin_site = MyAdminSite(name='myadmin')
# FIN DE DESACTIVAR ACCIONES RECIENTES


#-------------------------------------------------------------------------------------------------
#-------------------Especilidades se registran con el profesor------------------------------------
#-------------------------------------------------------------------------------------------------
class AsignaturasInline(admin.StackedInline):
    model=AsignaturasProfesor
    extra=0
#-------------------------------------------------------------------------------------------------
#----------------------------------------Presentacion de Profesores-------------------------------
#-------------------------------------------------------------------------------------------------
class ProfesorAdmin(admin.ModelAdmin):
    form=ProfesorForm
    inlines=[AsignaturasInline]
    search_fields=['rut','nombre','apellido']
    list_display=['id','rut','nombre','apellido','nivel','email','Foto']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name="PSICOLOGO").exists():
            return qs
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(id=request.user.id)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Si el objeto es nuevo (no existe aún en la base de datos)
            return ['nivel']
        return ['nivel']

#-------------------------------------------------------------------------------------------------
#-----------------------------------------Presentacion de Cursos---------------------------------
#-------------------------------------------------------------------------------------------------
class CursoAdmin(admin.ModelAdmin):
    form=CursoForm
    search_fields=['nombre']
    list_display=['id','nombre']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #if request.user.is_superuser:
        #    return qs  # Si es superusuario, mostrar todos los productos
        #return qs.filter(Profesor=request.user)  # Filtrar por usuario logueado
        return qs
#-------------------------------------------------------------------------------------------------
#----------------------------------------Presentacion de Asignaturas------------------------------
#-------------------------------------------------------------------------------------------------
class AsignaturaAdmin(admin.ModelAdmin):
    form=AsignaturaForm
    search_fields=['codigo','nombre']
    list_display=['id','codigo','nombre','curso_id']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #if request.user.is_superuser:
        #    return qs  # Si es superusuario, mostrar todos los productos
        #return qs.filter(Profesor=request.user)  # Filtrar por usuario logueado
        return qs
#-------------------------------------------------------------------------------------------------
#----------------------------------------Presentacion de Especialidades---------------------------
#-------------------------------------------------------------------------------------------------
class AsignaturasProfesorAdmin(admin.ModelAdmin):
    form=AsignaturasProfesorForm
    search_fields=['nombre']
    list_display=['id','nombre','profesor_id']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs

        return qs.filter(profesor_id=request.user.id)  # Filtrar por usuario logueado

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Si el objeto es nuevo (no existe aún en la base de datos)
            return ['nivel']  # Campo de solo lectura en nuevos registros
        return ['nivel']
#-------------------------------------------------------------------------------------------------
#---------------------------------------Presentacion de Disponibilida-----------------------------
#-------------------------------------------------------------------------------------------------
class DisponibilidadProfesorAdmin(admin.ModelAdmin):
    form=DisponibilidadProfesorForm
    search_fields=['estado','dia','bloque']
    list_display=['id','bloque','dia','estado','profesor_id']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(profesor_id=request.user.id)  # Filtrar por usuario logueado
#-------------------------------------------------------------------------------------------------
#--------------------------------------Presentacion de Horario------------------------------------
#-------------------------------------------------------------------------------------------------
class HorarioAdmin(admin.ModelAdmin):
    form=HorarioForm
    list_display=['id','bloque','dia','asignatura_id','curso_id','profesor_id']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(profesor_id=request.user.id)  # Filtrar por usuario logueado
#-------------------------------------------------------------------------------------------------
#-----------------------------------------Presentacion de Actividades-----------------------------
#-------------------------------------------------------------------------------------------------
class ActividesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.Profesor = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

    form=ActividadesForm
    list_display=['get_profesor_nombre','Tipo','Nombre','FechaHoraRegistro','FechaHoraPlanificada','NumeroParticipantesActividad']
    search_fields=['get_profesor_nombre','Tipo','Nombre']

    def get_profesor_nombre(self, obj):
        return f"{obj.Profesor.first_name} {obj.Profesor.last_name}"

    get_profesor_nombre.short_description='Profesor'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(Profesor_id = request.user.id)  # Filtrar por usuario logueado

#-------------------------------------------------------------------------------------------------
#----------------------------------------Presentacion de Atenciones-------------------------------
#-------------------------------------------------------------------------------------------------
class AtencionesAdmin(admin.ModelAdmin):
    form=AtencionesForm
    list_display=['id','Tipo','get_profesor_nombre','FechaHoraRegistro','get_alumno_nombre','Motivo']
    search_fields=['get_profesor_nombre','get_alumno_nombre','Motivo']

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.Profesional = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

    def get_profesor_nombre(self, obj):
        return f"{obj.Profesional.first_name} {obj.Profesional.last_name}"

    get_profesor_nombre.short_description='Profesional'

    def get_alumno_nombre(self, obj):
        return f"{obj.idMatricula.run} / {obj.idMatricula.nombre} {obj.idMatricula.apellido_paterno}"
    get_alumno_nombre.short_description='idMatricula'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(Profesional_id=request.user.id)  # Filtrar por usuario logueado
    class Media:
        js=('horarios/static/js/custom_admin.js',)
#-------------------------------------------------------------------------------------------------
#--------------------------------------Presentacion de Insumos------------------------------------
#-------------------------------------------------------------------------------------------------
class InsumosAdmin(admin.ModelAdmin):
    form = InsumosForm
    list_display=['IdInsumo','NombreInsumo','DetalleInsumo','StockInsumo','EstadoInsumo']
    search_fields=['NombreInsumo','DetalleInsumo']

#-------------------------------------------------------------------------------------------------
#-----------------------------------Presentacion de Prestamos-------------------------------------
#-------------------------------------------------------------------------------------------------
class PrestamosAdmin(admin.ModelAdmin):
    list_display=['get_profesor_nombre','FechaHoraRegistroPrestamo','FechaHoraDevolucionPrestamo','EstadoPrestamo']
    search_fields=['get_profesor_nombre']

    form = PrestamosForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.Administrativo = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

    def get_profesor_nombre(self, obj):
        return f"{obj.Administrativo.first_name} {obj.Administrativo.last_name}"

    get_profesor_nombre.short_description='Administrativo'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Si el objeto es nuevo (no existe aún en la base de datos)
            return ['EstadoPrestamo']  # Campo de solo lectura en nuevos registros
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(Administrativo_id=request.user.id)  # Filtrar por usuario logueado
#-------------------------------------------------------------------------------------------------
#-------------------------------------Presentacion de Certificados--------------------------------
#-------------------------------------------------------------------------------------------------
class CertificadosAdmin(admin.ModelAdmin):
    form=CertificadosForm
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.Administrativo = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

    def get_alumno_nombre(self, obj):
        return f"{obj.idMatricula.run} / {obj.idMatricula.nombre} {obj.idMatricula.apellido_paterno}"
    get_alumno_nombre.short_description='idMatricula'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(Administrativo_id=request.user.id)  # Filtrar por usuario logueado

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Si el objeto es nuevo (no existe aún en la base de datos)
            return ['EstadoCertificado']  # Campo de solo lectura en nuevos registros
        return []
    #list_display=['idCertificado','idMatriculaEstudiante','TipoCertificado','MotivoCertificado','LugarPresentacionCertificado','Administrativo','FechaHoraRegistroCertificado','EstadoCertificado']
    list_display=['idCertificado','get_alumno_nombre','TipoCertificado','FechaHoraRegistroCertificado','EstadoCertificado']
    search_fields=['get_alumno_nombre','TipoCertificado']

    actions=['generar_certificados']

    def generar_certificados(modeladmin, request, queryset):
        # Crear un archivo ZIP para contener los PDFs
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for certificado in queryset:
                # Crear un buffer para cada PDF
                buffer = io.BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)

                # Dimensiones de la página
                width, height = letter

                # Ruta al logo del establecimiento
                logo_path = os.path.join("home","greystatistic","Sistema_Educacional","staticfiles", "imagenes", "logo.PNG")

                # Agregar el logo al PDF
                if os.path.exists(logo_path):
                    p.drawImage(logo_path, 50, height - 100, width=100, height=50)  # Ajusta posición y tamaño según tus necesidades

                # Acceder a los datos del alumno a través de la FK
                alumno = certificado.idMatricula

                # Agregar texto al PDF
                titulo = f"Certificado de {certificado.TipoCertificado}"
                titulo_ancho = p.stringWidth(titulo, "Helvetica-Bold", 16)
                p.drawString((width - titulo_ancho) / 2, height - 50, titulo)

                p.setFont("Helvetica", 12)
                p.drawString(100, height - 150, f"Nombre: {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
                p.drawString(100, height - 170, f"Curso: {alumno.curso}")
                p.drawString(100, height - 190, "----------------------------")

                # Finalizar el PDF
                p.save()
                buffer.seek(0)

                # Crear un nombre de archivo único
                pdf_filename = f"certificado_{Certificados.idCertificado}.pdf"

                # Agregar el PDF al archivo ZIP
                zip_file.writestr(pdf_filename, buffer.getvalue())

        # Finalizar el archivo ZIP
        zip_buffer.seek(0)

        # Retornar el archivo ZIP como respuesta
        return FileResponse(zip_buffer, as_attachment=True, filename="certificados.zip")
#-------------------------------------------------------------------------------------------------
#-----------------------------Presentacion de Consejo de Profesores-------------------------------
#-------------------------------------------------------------------------------------------------
class ConsejosProfesoresAdmin(admin.ModelAdmin):
    form = ConsejosProfesoresForm
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.Administrativo = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

    list_display=['idConsejo','get_profesor_nombre','FechaHoraPlanificadaConsejo','NumeroProfesoresConsejo']
    search_fields=['get_profesor_nombre','FechaHoraPlanificadaConsejo']

    def get_profesor_nombre(self, obj):
        return f"{obj.Administrativo.first_name} {obj.Administrativo.last_name}"

    get_profesor_nombre.short_description='Administrativo'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="PROFESORES").exists():
            return qs
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(Administrativo_id=request.user.id)  # Filtrar por usuario logueado
#-------------------------------------------------------------------------------------------------
#---------------------------------------Presentacion de Impresiones------------------------------------
#-------------------------------------------------------------------------------------------------
class ImpresionesAdmin(admin.ModelAdmin):
    form = ImpresionesForm
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.ProfesorImpresion = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

    list_display=['get_profesor_nombre','FechaHoraRegistroImpresion','FechaHoraUtilizacionImpresion','CursoImpresion','AsignaturaImpresion','ObservacionImpresion','EstadoImpresion']
    search_fields=['get_profesor_nombre','CursoImpresion','AsignaturaImpresion']

    def get_profesor_nombre(self, obj):
        return f"{obj.ProfesorImpresion.first_name} {obj.ProfesorImpresion.last_name}"

    get_profesor_nombre.short_description='ProfesorImpresion'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Si el objeto es nuevo (no existe aún en la base de datos)
            return ['EstadoImpresion']  # Campo de solo lectura en nuevos registros
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, mostrar todos los productos
        if request.user.groups.filter(name="UTP").exists():
            return qs
        if request.user.groups.filter(name="ADMINISTRADOR").exists():
            return qs
        return qs.filter(ProfesorImpresion_id=request.user.id)  # Filtrar por usuario logueado
#-------------------------------------------------------------------------------------------------
#----------------------------------Padres se registran con Alumno---------------------------------
#-------------------------------------------------------------------------------------------------
class PadreInline(admin.StackedInline):
    model=Padre
    form=PadreForm
    extra=1
    max_num=2
    exclude=['alumno_id','id']
    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
#-------------------------------------------------------------------------------------------------
#-----------------------------Apoderados se registran con Alumno----------------------------------
#-------------------------------------------------------------------------------------------------
class ApoderadoInline(admin.StackedInline):
    model=Apoderado
    form=ApoderadoForm
    extra=1
    max_num=2
    exclude=['alumno_id','id']
    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
#-------------------------------------------------------------------------------------------------
#--------------------------------------Presentacion de Apoderados---------------------------------
#-------------------------------------------------------------------------------------------------
class ApoderadoAdmin(admin.ModelAdmin):
    list_display=['run','nombre','apellido_paterno','apellido_materno','fono','get_alumno_nombre']
    def get_alumno_nombre(self, obj):
        return f"{obj.alumno.run} / {obj.alumno.nombre} {obj.alumno.apellido_paterno}"

    get_alumno_nombre.short_description='alumno'
    actions=None
#-------------------------------------------------------------------------------------------------
#------------------------------------Presentacion de Alumnos--------------------------------------
#-------------------------------------------------------------------------------------------------
class AlumnoAdmin(admin.ModelAdmin):

     # Filtrar por usuario logueado

    def save_model(self, request, obj, form, change):
        obj.administrativo = request.user # Asigna el usuario autenticado al campo profesor
        super().save_model(request, obj, form, change)

        def save_related(self, request, obj, form, formsets, change):
            super().save_related(request, obj, form, formsets, change)
            for formset in formsets:
                instances = formset.save
                for instance in instances:
                    instance.alumno = obj
                    instance.save()
                formset.save_m2m()
    
    ordering=['matricula']



    actions=['exportar_a_excel']

    def exportar_a_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Matriculas de Alumnos'

        # Agregar encabezados del modelo principal (Alumnos)
        headers = [field.verbose_name for field in Alumnos._meta.fields if field.name != 'Administrativo' and field.name != 'Foto']

        # Agregar encabezados adicionales para inlines (Padres y Apoderados)
        headers += ['Padre o Madre', 'Run Padre', 'Nombre Padre', 'Apellido Paterno Padre', 'Apellido Materno Padre', 'Fono Padre', 'Escolaridad Padre', 'Edad Padre', 'Ocupacion Padre', 'Religion Padre', 'Run Apoderado', 'Nombre Apoderado', 'Apellido Paterno Apoderado', 'Apellido Materno Apoderado', 'Fono Apoderado', 'Escolaridad Apoderado', 'Edad Apoderado', 'Ocupacion Apoderado', 'Religion Apoderado']

        # Agregar encabezados a la hoja de Excel
        ws.append(headers)

        for obj in queryset:
            # Datos del modelo principal (Alumnos)
            alumno_data = []
            for field in Alumnos._meta.fields:
                value = getattr(obj, field.name)
                if field.name != 'Administrativo' and field.name != 'Foto':
                    # Si es la fecha, convertirla a número de serie de Excel
                    if field.name == 'FechaHoraRegistroMatriculaEstudiante':
                        value = str(value)  # Convertir la fecha a formato numérico de Excel
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

    exportar_a_excel.short_description = "Exportar a Excel"


    form=AlumnoForm
    inlines=[PadreInline, ApoderadoInline]
    list_display=['matricula','curso','run','nombre','apellido_paterno','apellido_materno','direccion','comuna','procedencia','curso_repetido','con_quien_vive','enfermedad','prevision','letra_fonasa','alimentacion_establecimiento','programa_solidario','programa','locomocion','fono_locomocion','vive_con','emergencia','complementarios','Foto']
    search_fields=['run','nombre','apellido_paterno','apellido_materno']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #if request.user.is_superuser:
        #    return qs  # Si es superusuario, mostrar todos los productos
        #return qs.filter(Administrativo_id=request.user)
        return qs  # Si es superusuario, mostrar todos los productos

    class Media:
        js = ('horarios/static/admin/js/custom.js',)
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
admin.site.register(Alumnos, AlumnoAdmin)
admin.site.register(Usuario)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(AsignaturasProfesor, AsignaturasProfesorAdmin)
admin.site.register(DisponibilidadProfesor, DisponibilidadProfesorAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Impresiones, ImpresionesAdmin)
admin.site.register(ConsejosProfesores, ConsejosProfesoresAdmin)
admin.site.register(Prestamos, PrestamosAdmin)
admin.site.register(Insumos, InsumosAdmin)
admin.site.register(Atenciones, AtencionesAdmin)
admin.site.register(Actividades, ActividesAdmin)
admin.site.register(Certificados, CertificadosAdmin)
admin.site.register(Apoderado, ApoderadoAdmin)