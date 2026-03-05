"""
URL configuration for Sistema_Educacional project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from horarios import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
#-----------------General----------------------------------------------------------------------------
    path('admin/', admin.site.urls),
    path('',views.mostrarIndex,name='login'),
    path('login',views.iniciarSesion),
    path('logout',views.cerrarSesion,name='logout'),
    path('registrar',views.registrar,name='registrar'),
    path('registrar_usu',views.registrarUsuarios),
    path('registrar_cur',views.registrarCursos),
    path('visualizar_horarios',views.mostrarVisualizarHorario),
    path('visualizar_disponibilidad',views.mostrarVisualizarDisp),
    path('buscar_dis/<str:hash_id>',views.buscarProfesorDis,name='buscar_dis'),
    path('buscar_cur',views.buscarCurso),
    path('visualizar_horarios_profesores',views.mostrarHorarioProfesor),
    path('buscar_pro',views.buscarProfesor),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('otp',views.verify_otp,name='otp'),
    path('resend_otp',views.resend_otp,name='resend_otp'),
    path('reset_password',views.reset_password,name='reset_password'),
#---------------------------Directora---------------------------------------------------------------
    path('menu',views.mostrarMenu, name='menu'),
    path('visualizar_historial',views.mostrarHistorial),
#---------------------------Secretaria---------------------------------------------------------------
    #-----------------------Asignaturas-----------------------------------------
    path('registrar_asignaturas',views.mostrarRegistrarAsig,name='registrar_asignaturas'),
    path('modificar_asignatura/<str:hash_id>',views.mostrarModificarAsig,name='modificar_asignatura'),
    path('registrar_asg',views.registrarAsignatura,name='registrar_asg'),
    path('modificar_asg/<str:hash_id>',views.modificarAsignatura,name='modificar_asg'),
    path('eliminar_asg/<str:hash_id>',views.eliminarAsignatura,name='eliminar_asg'),
    #---------------------Profesores---------------------------------------------
    path('registrar_profesor',views.mostrarRegistrarPro, name='registrar_profesor'),
    path('modificar_profesor/<str:hash_id>',views.mostrarModificarPro, name='modificar_profesor'),
    path('registrar_pro',views.registrarProfesor, name='registrar_pro'),
    path('modificar_pro/<str:hash_id>',views.modificarProfesor, name='modificar_pro'),
    path('eliminar_pro/<str:hash_id>',views.eliminarProfesor, name='eliminar_pro'),
    #--------------------Horarios-------------------------------------------------
    path('registrar_horarios',views.mostrarRegistrarHor, name='registrar_horarios'),
    path('mostrar_horario/<str:hash_id>',views.mostrarHorario, name='mostrar_horario'),
    path('cambiar_hor/<int:id>/<int:idc>',views.cambiarHorario, name='cambiar_hor'),
    #--------------------Disponibilidad------------------------------------------
    path('registrar_disponibilidad/<str:hash_id>',views.mostrarRegistrarDis, name='registrar_disponibilidad'),
    path('cambiar_disponibilidad/<int:id>/<int:id2>',views.cambiarDisponibilidad, name='cambiar_disponibilidad'),
    #------------------Especialidades (Asignaturas) Porfesor-----------------------------------------------
    path('registrar_especialidad/<str:hash_id>',views.mostrarRegistrarEsp, name='registrar_especialidad'),
    path('registrar_esp/<str:hash_id>',views.registrarEspecialidad, name='registrar_esp'),
    path('eliminar_esp/<int:id>/<int:id2>',views.eliminarEspecialidad, name='eliminar_esp'),
#---------------------------Exportación y Reportes-----------------------------------------------
    path('listar_alumnos',views.listar_alumnos, name='listar_alumnos'),
    path('exportar_alumnos_excel',views.exportar_alumnos_excel, name='exportar_alumnos_excel'),
    path('listar_certificados',views.listar_certificados, name='listar_certificados'),
    path('generar_certificados_pdf',views.generar_certificados_pdf, name='generar_certificados_pdf'),
    path('mostrar_registrar_certificado',views.mostrar_registrar_certificado, name='mostrar_registrar_certificado'),
    path('registrar_certificado',views.registrar_certificado, name='registrar_certificado'),
#---------------------------Registro de Alumnos-----------------------------------------------
    path('registrar_alumno',views.registrar_alumno, name='registrar_alumno'),
    path('perfil',views.mostrar_perfil, name='perfil'),
    path('cambiar_password',views.cambiar_password, name='cambiar_password'),
#---------------------------Gestión de Actividades-----------------------------------------------
    path('listar_actividades',views.listar_actividades, name='listar_actividades'),
    path('registrar_actividad',views.mostrar_registrar_actividad, name='mostrar_registrar_actividad'),
    path('mostrar_registrar_actividad',views.mostrar_registrar_actividad),
    path('registrar_actividad_post',views.registrar_actividad, name='registrar_actividad'),
    path('modificar_actividad/<str:hash_id>',views.mostrar_modificar_actividad, name='mostrar_modificar_actividad'),
    path('modificar_actividad_post/<str:hash_id>',views.modificar_actividad, name='modificar_actividad'),
    path('eliminar_actividad/<str:hash_id>',views.eliminar_actividad, name='eliminar_actividad'),
    
    # URLs para Atenciones
    path('listar_atenciones/', views.listar_atenciones, name='listar_atenciones'),
    path('mostrar_registrar_atencion/', views.mostrar_registrar_atencion, name='mostrar_registrar_atencion'),
    path('registrar_atencion/', views.registrar_atencion, name='registrar_atencion'),
    path('mostrar_modificar_atencion/<str:hash_id>/', views.mostrar_modificar_atencion, name='mostrar_modificar_atencion'),
    path('modificar_atencion/<str:hash_id>/', views.modificar_atencion, name='modificar_atencion'),
    path('eliminar_atencion/<str:hash_id>/', views.eliminar_atencion, name='eliminar_atencion'),
    
    # URLs para gestión de Insumos
    path('insumos/', views.listar_insumos, name='listar_insumos'),
    path('insumos/registrar/', views.mostrar_registrar_insumo, name='mostrar_registrar_insumo'),
    path('insumos/registrar/procesar/', views.registrar_insumo, name='registrar_insumo'),
    path('insumos/modificar/<int:id_insumo>/', views.mostrar_modificar_insumo, name='mostrar_modificar_insumo'),
    path('insumos/modificar/procesar/', views.modificar_insumo, name='modificar_insumo'),
    path('insumos/eliminar/<int:id_insumo>/', views.eliminar_insumo, name='eliminar_insumo'),

    # URLs para gestión de Préstamos
    path('listar_prestamos/', views.listar_prestamos, name='listar_prestamos'),
    path('mostrar_registrar_prestamo/', views.mostrar_registrar_prestamo, name='mostrar_registrar_prestamo'),
    path('registrar_prestamo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('mostrar_modificar_prestamo/<int:id_prestamo>/', views.mostrar_modificar_prestamo, name='mostrar_modificar_prestamo'),
    path('modificar_prestamo/', views.modificar_prestamo, name='modificar_prestamo'),
    path('eliminar_prestamo/<int:id_prestamo>/', views.eliminar_prestamo, name='eliminar_prestamo'),
    path('prestamos/eliminar/<int:id_prestamo>/', views.eliminar_prestamo, name='eliminar_prestamo_legacy'),
    
    # Consejos de Profesores
    path('consejos/', views.listar_consejos, name='listar_consejos'),
    path('listar_consejos/', views.listar_consejos, name='listar_consejos_legacy'),
    path('consejos/registrar/', views.mostrar_registrar_consejo, name='mostrar_registrar_consejo'),
    path('consejos/registrar/procesar/', views.registrar_consejo, name='registrar_consejo'),
    path('consejos/modificar/<str:id_consejo>/', views.mostrar_modificar_consejo, name='mostrar_modificar_consejo'),
    path('consejos/modificar/<str:id_consejo>/procesar/', views.modificar_consejo, name='modificar_consejo'),
    path('consejos/eliminar/<str:id_consejo>/', views.eliminar_consejo, name='eliminar_consejo'),
    
    # Impresiones
    path('impresiones/', views.listar_impresiones, name='listar_impresiones'),
    path('impresiones/registrar/', views.mostrar_registrar_impresion, name='mostrar_registrar_impresion'),
    path('impresiones/registrar/procesar/', views.registrar_impresion, name='registrar_impresion'),
    path('impresiones/modificar/<str:id_impresion>/', views.mostrar_modificar_impresion, name='mostrar_modificar_impresion'),
    path('impresiones/modificar/<str:id_impresion>/procesar/', views.modificar_impresion, name='modificar_impresion'),
    path('impresiones/eliminar/<str:id_impresion>/', views.eliminar_impresion, name='eliminar_impresion'),
    
    # URLs para Padres/Apoderados
    path('listar_padres/', views.listar_padres, name='listar_padres'),
    path('mostrar_registrar_padre/', views.mostrar_registrar_padre, name='mostrar_registrar_padre'),
    path('registrar_padre/', views.registrar_padre, name='registrar_padre'),
    path('mostrar_modificar_padre/<int:id_padre>/', views.mostrar_modificar_padre, name='mostrar_modificar_padre'),
    path('modificar_padre/<int:id_padre>/', views.modificar_padre, name='modificar_padre'),
    path('eliminar_padre/<int:id_padre>/', views.eliminar_padre, name='eliminar_padre'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
