from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from .models import Profesor, Asignatura, Curso, AsignaturasProfesor, DisponibilidadProfesor, Horario, Usuario, Historial, Alumnos, Padre, Apoderado, Impresiones, Insumos, Prestamos, ConsejosProfesores, CURSOS_CHOICE, ESTADOIMPRESION_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .decorators import role_required, profesor_data_only, alumno_data_only, login_or_session_required

#----------------------------------------------------------------------
#permite visualizar la pagina de login.
def mostrarIndex(request):
    us=Usuario.objects.all().values()
    cur=Curso.objects.all().values()
    if us:
        if cur:
            usu=Usuario.objects.all().order_by("id")
            datos={"uc":'Cursos y Usuarios cargados correctamente!!',"usu":usu}
            return render(request,'index.html',datos)
        else:
            datos={"c":'Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"u":'Debe cargar los Usuarios y las Cursos'}
        return render(request,'index.html',datos)
#----------------------------------------------------------------------
def registrarUsuarios(request):

    if request.method=="POST":
        nom1="DIRECTOR"
        nom2="SECRETARIA"
        pas1="123"
        user = User.objects.create_user(nom1, 'c@example.com', pas1)
        user.save()
        u=Usuario(nombre=nom1,password=pas1,cargo="DIRECTOR",user=user)
        u.save()
        user = User.objects.create_user(nom2, 'c@example.com', pas1)
        user.save()
        us=Usuario(nombre=nom2,password=pas1,cargo="SECRETARIA",user=user)
        us.save()
        datos={"r":'Usuarios creados correctamente!!',"c":'Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
    else:
        datos={"r2":'Error al realizar solicitud!!'}
        return render(request,'index.html',datos)
#-----------------------------------------------------------------------
def registrarCursos(request):
    if request.method=="POST":
        nom1="PRIMERO BASICO"
        nom2="SEGUNDO BASICO"
        nom3="TERCERO BASICO"
        nom4="CUARTO BASICO"
        nom5="QUINTO BASICO"
        nom6="SEXTO BASICO"
        nom7="SEPTIMO BASICO"
        nom8="OCTAVO BASICO"
        nom9="PRIMERO MEDIO"                                       #Registra todos los cursos con sus horarios vacios, listos para ser editados
        nom10="SEGUNDO MEDIO"                                      #Desde la Linea 37 hasta la 1074.
        nom11="TERCERO MEDIO"
        nom12="CUARTO MEDIO"
        nom13="KINDER"
        nom14="PRE-KINDER"
        c=Curso(nombre=nom1)
        c.save()
        c=Curso(nombre=nom2)
        c.save()
        c=Curso(nombre=nom3)
        c.save()
        c=Curso(nombre=nom4)
        c.save()
        c=Curso(nombre=nom5)
        c.save()
        c=Curso(nombre=nom6)
        c.save()
        c=Curso(nombre=nom7)
        c.save()
        c=Curso(nombre=nom8)
        c.save()
        c=Curso(nombre=nom9)
        c.save()
        c=Curso(nombre=nom10)
        c.save()
        c=Curso(nombre=nom11)
        c.save()
        c=Curso(nombre=nom12)
        c.save()
        c=Curso(nombre=nom13)
        c.save()
        c=Curso(nombre=nom14)
        c.save()
        c=Curso.objects.get(nombre=nom1)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom2)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()


        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom3)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom4)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom5)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom6)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom7)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom8)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom9)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom10)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom11)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom12)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()

        c=Curso.objects.get(nombre=nom13)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()


        c=Curso.objects.get(nombre=nom14)
        id=c.id
        h=Horario(bloque=1,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="LUNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="LUNES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MARTES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MARTES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="MIERCOLES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="MIERCOLES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="JUEVES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="JUEVES",curso_id=id)
        h.save()

        h=Horario(bloque=1,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=2,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=3,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=4,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=5,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=6,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=7,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=8,dia="VIERNES",curso_id=id)
        h.save()
        h=Horario(bloque=9,dia="VIERNES",curso_id=id)
        h.save()
        datos={"r":'Cursos cargados correctamente!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
    else:
        datos={"r2":'Error al realizar solicitud!!'}
        return render(request,'index.html',datos)
#-----------------------------------------------------------------
def registrar(request):
    if request.method=="POST":
        pas = request.POST["password"]
        pas2 = request.POST["confirm_password"]
        if pas!=pas2:
            datos={"r2":'Las contraseñas no coinciden',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'registrar.html',datos)
        nom = request.POST["username"]
        email = request.POST["email"]
        cargo = request.POST["cargo"]
        
        if Usuario.objects.filter(nombre=nom).exists():
            datos={"r2":'El usuario ya existe',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'registrar.html',datos)
        
        if cargo!="DIRECTOR" or cargo!="ADMINISTRADOR":
            # Create Django User model instance
            user = User.objects.create_user(
                username=nom,
                password=pas,
                email=email,
                is_staff=True,
                is_superuser=False
            )
        else:
            user = User.objects.create_user(
                username=nom,
                password=pas,
                email=email,
                is_staff=True,
                is_superuser=True
            )
        
        
        # Create custom Usuario model instance linked to Django User
        Usuario.objects.create(
            nombre=nom,
            password=pas,
            cargo=cargo,
            user=user
        )

        try:
            if cargo=="ESTUDIANTE":
                from .models import Alumnos
                alumno = Alumnos.objects.filter(email=email).first()
                if alumno:
                    alumno.user = user
                    alumno.save()
        except Exception:
            pass
        
        datos = {
            "r": "Usuario registrado correctamente",
            "uc": "Cursos y Usuarios cargados correctamente!!"
        }
        return render(request, 'index.html', datos)
        
    else:
        # Show registration form
        datos = {
            "r2": 'Complete el formulario para registrarse',
            "uc": 'Cursos y Usuarios cargados correctamente!!'
        }
        return render(request, 'registrar.html', datos)
#-----------------------------------------------------------------
def iniciarSesion(request):
    if request.method=="POST":
        nom=request.POST["txtusu"]
        pas=request.POST["txtpas"]
        if Usuario.objects.filter(nombre=nom,password=pas).exists():
            DatoUsuario=Usuario.objects.filter(nombre=nom).values()
            request.session["idUsuario"]=DatoUsuario[0]["id"]   
            request.session["idAuthUser"]=DatoUsuario[0]["user_id"]
            request.session["nomUsuario"]=nom.upper()
            request.session["pasUsuario"]=pas
            request.session["cargoUsuario"]=DatoUsuario[0]["cargo"]
            datos={'nomUsuario':nom.upper()}
            cargoUsuario=request.session.get("cargoUsuario")
            des="Inicio de Sesion "+str(nom)+""
            tabla=""
            fyh=timezone.now()
            usuario=request.session.get("idUsuario")
            his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
            his.save()
            
            if cargoUsuario=="PROFESOR":
                idAuthUser=request.session.get("idAuthUser")
                datpro=Profesor.objects.filter(usuario_id=idAuthUser).values()
                if not datpro:
                    datpro=Profesor.objects.filter(email=nom.lower()).values()
                if datpro:
                    espro=AsignaturasProfesor.objects.filter(profesor_id=datpro[0]['id'])
                    datos={"cargo":cargoUsuario,"nomUsuario":nom.upper(),"datpro":datpro,"espro":espro}
                else:
                    datos={"cargo":cargoUsuario,"nomUsuario":nom.upper()}
            elif cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
                idAuthUser=request.session.get("idAuthUser")
                datest=Alumnos.objects.filter(user_id=idAuthUser).values()
                if not datest:
                    datest=Alumnos.objects.filter(email__iexact=nom).values()
                if not datest and hasattr(request, "user") and getattr(request.user, "email", None):
                    datest=Alumnos.objects.filter(email__iexact=request.user.email).values()
                if not datest:
                    datest=Alumnos.objects.filter(run__iexact=nom).values()
                if datest:
                    pad=Padre.objects.filter(alumno_id=datest[0]['matricula'])
                    apo=Apoderado.objects.filter(alumno_id=datest[0]['matricula'])
                    datos={"cargo":cargoUsuario,"nomUsuario":nom.upper(),"datest":datest,"pad":pad,"apo":apo}
                else:
                    datos={"cargo":cargoUsuario,"nomUsuario":nom.upper()}
            else:
                datos={"cargo":cargoUsuario,"nomUsuario":nom.upper()}
            return render(request,'menu.html',datos)
        else:
            datos={"r2":'Error de Usuario y/o contraseña',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe presionar el boton de inicio de sesion',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#------------------------------------------------------------------
def mostrarMenu(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="PROFESOR":
            idAuthUser=request.session.get("idAuthUser")
            datpro=Profesor.objects.filter(usuario_id=idAuthUser).values()
            if not datpro:
                datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
            if datpro:
                espro=AsignaturasProfesor.objects.filter(profesor_id=datpro[0]['id'])
                datos={"cargo":cargoUsuario,"nomUsuario":nomUsuario,"datpro":datpro,"espro":espro}
            else:
                datos={"cargo":cargoUsuario,"nomUsuario":nomUsuario}
        elif cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
            idAuthUser=request.session.get("idAuthUser")
            datest=Alumnos.objects.filter(user_id=idAuthUser).values()
            if not datest:
                datest=Alumnos.objects.filter(email__iexact=nomUsuario).values()
            if not datest and hasattr(request, "user") and getattr(request.user, "email", None):
                datest=Alumnos.objects.filter(email__iexact=request.user.email).values()
            if not datest:
                datest=Alumnos.objects.filter(run__iexact=nomUsuario).values()
            if datest:
                pad=Padre.objects.filter(alumno_id=datest[0]['matricula'])
                apo=Apoderado.objects.filter(alumno_id=datest[0]['matricula'])
                datos={"cargo":cargoUsuario,"nomUsuario":nomUsuario,"datest":datest,"pad":pad,"apo":apo}
            else:
                datos={"cargo":cargoUsuario,"nomUsuario":nomUsuario}
        else:
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario}
        return render(request,'menu.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------
def cerrarSesion(request):
    try:
        nom=request.session.get("nomUsuario")
        des="Cierre de Sesion "+str(nom)+""
        tabla=""
        fyh=timezone.now()
        usuario=request.session.get("idUsuario")
        his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
        his.save()
        del request.session["idUsuario"]
        del request.session["nomUsuario"]
        del request.session["pasUsuario"]
        del request.session["cargoUsuario"]
        datos={"r":'Sesion cerrada correctamente',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
    except:
        datos={"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#------------Asignaturas-------------------------------------------------------
def mostrarRegistrarAsig(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
            cur=Curso.objects.all()
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"asg":asg}
            return render(request,'registrar_asignatura.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder al registro de Asignaturas!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------
def mostrarModificarAsig(request, hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            id=Asignatura.decode_hash(hash_id)
            rs=Asignatura.objects.select_related("curso").filter(id=id)
            if rs:
                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                cur=Curso.objects.all()
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"asg":asg,"rs":rs,"cur":cur}
                return render(request,'modificar_asignatura.html',datos)
            else:
                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                cur=Curso.objects.all()
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"asg":asg,"r2":'Asignatura no disponible!!'}
                return render(request,'registrar_asignatura.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder al registro de Asignaturas!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------
def registrarAsignatura(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            if request.method=="POST":
                cod=request.POST["txtcod"].upper()
                mat=request.POST["opasg"]
                cur=request.POST["opcur"]
                comprobarAsignatura=Asignatura.objects.filter(codigo=cod.upper())
                cur=int(cur)
                if comprobarAsignatura:
                    asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")                          #Registra las Asignaturas y las evalua para determinar sus bloques semanales
                    cur=Curso.objects.all()                                                                                     #Desde la linea 1191 hasta la 1407
                    datos={"r2":'El codigo ya esta en uso!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                    return render(request,'registrar_asignatura.html',datos)
                else:
                    comprobarAsignatura=Asignatura.objects.filter(nombre=mat,curso_id=cur)
                    if comprobarAsignatura:
                        asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                        cur=Curso.objects.all()
                        datos={"nomUsuario":nomUsuario,"cur":cur,"asg":asg,"r2":'Asignatura ya Registrada para el curso seleccionado!!'}
                        return render(request,'registrar_asignatura.html',datos)
                    else:
                        if (mat=="Biología" or mat=="Química" or mat=="Física" or mat=="Filosofía y Psicología") and cur<=10 or mat=="Tecnología" and cur>=11:
                            asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                            cur=Curso.objects.all()
                            datos={"r2":'La asignatura no corresponde al curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                            return render(request,'registrar_asignatura.html',datos)
                        else:
                            if cur<=8:
                                niv="BASICA"
                                if cur<=4 and mat=="Idioma Extranjero: Inglés":
                                    asg=Asignatura.objects.select_related("curso").all().order_by("codigo")
                                    cur=Curso.objects.all()
                                    datos={"r2":'La asignatura no corresponde al curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                                    return render(request,'registrar_asignatura.html',datos)
                                else:
                                    if cur>=1 and cur<=4:
                                        if mat=="Lenguaje y Comunicación (1ero a 4to Basico) - 8hrs":
                                            blo=8
                                        if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                            blo=6
                                        if mat=="Historia, Geografía y Ciencias Sociales (1ero a 4to Basico) - 3hrs":
                                            blo=3
                                        if mat=="Artes Visuales (1ero a 4to Basico) - 2hrs":
                                            blo=2
                                        if mat=="Música  (1ero a 4to Basico) - 2hrs":
                                            blo=2
                                        if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                            blo=2
                                        if mat=="Orientación  (1ero a 4to Basico) - 1hr":
                                            blo=1
                                        if mat=="Tecnología  (1ero a 4to Basico) - 1hr":
                                            blo=1
                                        if mat=="Religión (Todas) - 2hrs":
                                            blo=2
                                        if mat=="Ciencias Naturales (1ero a 6to Basico) - 3hrs":
                                            blo=3
                                        if mat=="Inglés (Libre Disposicion)  (1ero a 4to Basico) - 1hr":
                                            blo=1
                                    if cur==5 or cur==6:
                                        if mat=="Lenguaje y Comunicación  (5to y 6to Basico) - 6hrs":
                                            blo=6
                                        if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                            blo=6
                                        if mat=="Historia, Geografía y Ciencias Sociales  (5to a 2do Medio) - 4hrs":
                                            blo=4
                                        if mat=="Artes Visuales (5to a 6to Basico) - 1hr":
                                            blo=1
                                        if mat=="Música  (5to y 6to Basico) - 1hr":
                                            blo=1
                                        if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                            blo=2
                                        if mat=="Orientación  (5to a 2do Medio) - 1hr":
                                            blo=1
                                        if mat=="Tecnología  (5to a 2do Medio) - 1hr":
                                            blo=1
                                        if mat=="Religión (Todas) - 2hrs":
                                            blo=2
                                        if mat=="Ciencias Naturales (1ero a 6to Basico) - 3hrs":
                                            blo=3
                                        if mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                            blo=3
                                    if cur==7 or cur==8:
                                        if mat=="Lengua y Literatura (7mo a 2do Medio) - 6hrs":
                                            blo=6
                                        if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                            blo=6
                                        if mat=="Historia, Geografía y Ciencias Sociales  (5to a 2do Medio) - 4hrs":
                                            blo=4
                                        if mat=="Artes Visuales y Música (7mo y 8vo Basico) - 2hrs":
                                            blo=2
                                        if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                            blo=2
                                        if mat=="Orientación  (5to a 2do Medio) - 1hr":
                                            blo=1
                                        if mat=="Tecnología  (5to a 2do Medio) - 1hr":
                                            blo=1
                                        if mat=="Religión (Todas) - 2hrs":
                                            blo=2
                                        if mat=="Ciencias Naturales  (7mo y 8vo Basico) - 4hrs":
                                            blo=4
                                        if mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                            blo=3
                                    a=Asignatura(codigo=cod.upper(),nombre=mat,nivel=niv,bloques=blo,curso_id=cur)
                                    a.save()
                                    des="Registro de Asignatura "+str(cod)+""
                                    tabla="Asignatura"
                                    fyh=datetime.now()
                                    usuario=request.session.get("idUsuario")
                                    his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                    his.save()
                                    asg=Asignatura.objects.select_related("curso").all().order_by("codigo")
                                    cur=Curso.objects.all()
                                    datos={"r":'La asignatura se registro con exito',"asg":asg,"cur":cur,"nomUsuario":nomUsuario}
                                    return render(request,'registrar_asignatura.html',datos)
                            elif cur==13 or cur==14:
                                niv="PREBASICA"
                                if cur==13:
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Inglés Nivel Transicion (Prekinder y Kinder) - 1hr":
                                        blo=1
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Asignatura Kinder - 1hr":
                                        blo=1
                                else:
                                    if mat=="Asignatura PreKinder - 1hr":
                                        blo=1
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Inglés Nivel Transicion (Prekinder y Kinder) - 1hr":
                                        blo=1
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                a=Asignatura(codigo=cod.upper(),nombre=mat,nivel=niv,bloques=blo,curso_id=cur)
                                a.save()
                                des="Registro de Asignatura "+str(cod)+""
                                tabla="Asignatura"
                                fyh=datetime.now()
                                usuario=request.session.get("idUsuario")
                                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                his.save()
                                asg=Asignatura.objects.select_related("curso").all().order_by("codigo")
                                cur=Curso.objects.all()
                                datos={"r":'La asignatura se registro con exito',"asg":asg,"cur":cur,"nomUsuario":nomUsuario}
                                return render(request,'registrar_asignatura.html',datos)
                            else:
                                niv="MEDIA"
                                if cur==9 or cur==10:
                                    if mat=="Lengua y Literatura (7mo a 2do Medio) - 6hrs":
                                        blo=6
                                    if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                        blo=6
                                    if mat=="Historia, Geografía y Ciencias Sociales  (5to a 2do Medio) - 4hrs":
                                        blo=4
                                    if mat=="Artes Visuales o Música (1ero y 2do Medio) - 2hrs":
                                        blo=2
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Orientación  (5to a 2do Medio) - 1hr":
                                        blo=1
                                    if mat=="Tecnología  (5to a 2do Medio) - 1hr":
                                        blo=1
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                        blo=3
                                    if mat=="Ciencias Naturales  (1ero y 2do Medio) - 6hrs":
                                        blo=6
                                if cur==11 or cur==12:
                                    if mat=="Lengua y Literatura (3ero y 4to Medio) - 3hrs":
                                        blo=3
                                    if mat=="Matemática  (3ero y 4to Medio) - 3hrs":
                                        blo=3
                                    if mat=="Historia, Geografía y Ciencias Sociales (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                    if mat=="Artes (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Ciencias para la Ciudadanía (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Inglés (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                    if mat=="Filosofía (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                    if mat=="Electivo de lengua y literatura (3ero y 4to Medio) - 6hrs":
                                        blo=6
                                    if mat=="Electivo de historia (3ero y 4to Medio) - 6hrs":
                                        blo=6
                                    if mat=="Electivo de matematicas (3ero y 4to Medio) - 6hrs":
                                        blo=6
                                    if mat=="Electivo de biología (3ero y 4to Medio) - 6hrs":
                                        blo=6
                                    if mat=="Educación Ciudadana (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                    if mat=="Ciencias para la Ciudadanía (3ero y 4to Medio) - 2hrs":
                                        blo=2
                                a=Asignatura(codigo=cod.upper(),nombre=mat,nivel=niv,bloques=blo,curso_id=cur)
                                a.save()
                                des="Registro de Asignatura "+str(cod)+""
                                tabla="Asignatura"
                                fyh=datetime.now()
                                usuario=request.session.get("idUsuario")
                                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                his.save()
                                cur=Curso.objects.all()
                                asg=Asignatura.objects.select_related("curso").all().order_by("codigo")
                                datos={"r":'La asignatura se registro con exito',"asg":asg,"nomUsuario":nomUsuario,"cur":cur}
                                return render(request,'registrar_asignatura.html',datos)
            else:
                asg=Asignatura.objects.select_related("curso").all().order_by("codigo")
                cur=Curso.objects.all()
                datos={"nomUsuario":nomUsuario,"cur":cur,"asg":asg,"r2":'Debe presionar el boton para registrar!!'}
                return render(request,'registrar_asignatura.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder al registro de Asignatura!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-----------------------------------------------------------------------------------
def eliminarAsignatura(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            id=Asignatura.decode_hash(hash_id)
            asg=Asignatura.objects.filter(id=id)
            if asg:
                ag=Asignatura.objects.get(id=id)
                cod=ag.codigo
                h=Horario.objects.filter(asignatura_id=id)
                if h:
                    j=0
                    for x in h:
                        if x == h[j]:
                            y=Horario.objects.get(id=h[j].id)
                            y.profesor_id=""
                            y.asignatura_id=""
                            y.save()
                        j=j+1
                ag.habilitado = False
                ag.save()
                des="Eliminacion de Asignatura "+str(cod)+""
                tabla="Asignatura"
                fyh=datetime.now()
                usuario=request.session.get("idUsuario")
                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                his.save()
                asg=Asignatura.objects.select_related("curso").filter(habilitado=True).order_by("curso_id")
                cur=Curso.objects.all()
                datos={"r":'Asignatura eliminada Correctamente!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                return render(request,'registrar_asignatura.html',datos)
            else:
                asg=Asignatura.objects.select_related("curso").filter(habilitado=True).order_by("curso_id")
                cur=Curso.objects.all()
                datos={"r2":'la Asignatura no se pudo eliminar!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                return render(request,'registrar_asignatura.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-----------------------------------------------------------------------------------
def modificarAsignatura(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            if request.method=="POST":
                cod=request.POST["txtcod"].upper()
                mat=request.POST["opasg"]
                cur=request.POST["opcur"]
                comprobarCodigo=Asignatura.objects.filter(codigo=cod.upper())
                cur=int(cur)
                id=Asignatura.decode_hash(hash_id)
                if comprobarCodigo:
                    comprobarA=Asignatura.objects.filter(id=id,codigo=cod.upper())
                    if not comprobarA:
                        asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                        cur=Curso.objects.all()
                        datos={"r2":'Codigo ya en uso!!',"asg":asg,"cur":cur,"nomUsuario":nomUsuario}
                        return render(request,'modificar_asignatura.html',datos)
                
                if True:
                    a=Asignatura.objects.get(id=id)
                    a.codigo=cod.upper()
                    if (mat=="Biología" or mat=="Química" or mat=="Física" or mat=="Filosofía y Psicología") and cur<=10 or mat=="Tecnología" and cur>=11:
                            asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                            cur=Curso.objects.all()
                            datos={"r2":'La asignatura no corresponde al curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                            return render(request,'registrar_asignatura.html',datos)
                    else:
                        blo = 0
                        if cur<=8:
                            niv="BASICA"
                            if cur<=4 and mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                                cur=Curso.objects.all()
                                datos={"r2":'La asignatura no corresponde al curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                                return render(request,'registrar_asignatura.html',datos)
                            else:
                                if cur>=1 and cur<=4:
                                    if mat=="Lenguaje y Comunicación (1ero a 4to Basico) - 8hrs":
                                        blo=8
                                    if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                        blo=6
                                    if mat=="Historia, Geografía y Ciencias Sociales (1ero a 4to Basico) - 3hrs":
                                        blo=3
                                    if mat=="Artes Visuales (1ero a 4to Basico) - 2hrs":
                                        blo=2
                                    if mat=="Música  (1ero a 4to Basico) - 2hrs":
                                        blo=2
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Orientación  (1ero a 4to Basico) - 1hr":
                                        blo=1
                                    if mat=="Tecnología  (1ero a 4to Basico) - 1hr":
                                        blo=1
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Ciencias Naturales (1ero a 6to Basico) - 3hrs":
                                        blo=3
                                    if mat=="Inglés (Libre Disposicion)  (1ero a 4to Basico) - 1hr":
                                        blo=1
                                if cur==5 or cur==6:
                                    if mat=="Lenguaje y Comunicación  (5to y 6to Basico) - 6hrs":
                                        blo=6
                                    if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                        blo=6
                                    if mat=="Historia, Geografía y Ciencias Sociales  (5to a 2do Medio) - 4hrs":
                                        blo=4
                                    if mat=="Artes Visuales (5to a 6to Basico) - 1hr":
                                        blo=1
                                    if mat=="Música  (5to y 6to Basico) - 1hr":
                                        blo=1
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Orientación  (5to a 2do Medio) - 1hr":
                                        blo=1
                                    if mat=="Tecnología  (5to a 2do Medio) - 1hr":
                                        blo=1
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Ciencias Naturales (1ero a 6to Basico) - 3hrs":
                                        blo=3
                                    if mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                        blo=3
                                if cur==7 or cur==8:
                                    if mat=="Lengua y Literatura (7mo a 2do Medio) - 6hrs":
                                        blo=6
                                    if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                        blo=6
                                    if mat=="Historia, Geografía y Ciencias Sociales  (5to a 2do Medio) - 4hrs":
                                        blo=4
                                    if mat=="Artes Visuales y Música (7mo y 8vo Basico) - 2hrs":
                                        blo=2
                                    if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Orientación  (5to a 2do Medio) - 1hr":
                                        blo=1
                                    if mat=="Tecnología  (5to a 2do Medio) - 1hr":
                                        blo=1
                                    if mat=="Religión (Todas) - 2hrs":
                                        blo=2
                                    if mat=="Ciencias Naturales  (7mo y 8vo Basico) - 4hrs":
                                        blo=4
                                    if mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                        blo=3
                                h=Horario.objects.filter(asignatura_id=id)
                                if h:
                                    j=0
                                    for x in h:
                                        if x == h[j]:
                                            y=Horario.objects.get(id=h[j].id)
                                            y.profesor_id=""
                                            y.asignatura_id=""
                                            y.save()

                                        j=j+1

                                if blo == 0:
                                    asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                                    cur=Curso.objects.all()
                                    datos={"r2":'La asignatura no es válida para el curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                                    return render(request,'registrar_asignatura.html',datos)

                                cur=str(cur)
                                a.nombre=mat
                                a.nivel=niv
                                a.bloque=blo
                                a.curso_id=cur
                                a.save()
                                h=Horario.objects.filter(asignatura_id=id)

                                des="Modificacion de Asignatura "+str(cod)+""
                                tabla="Asignatura"
                                fyh=datetime.now()
                                usuario=request.session.get("idUsuario")
                                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                his.save()
                                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                                cur=Curso.objects.all()
                                datos={"r":'Asignatura modificada Correctamente!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                                return render(request,'registrar_asignatura.html',datos)
                        elif cur==13 or cur==14:
                            niv="PREBASICA"
                            if cur==13:
                                if mat=="Religión (Todas) - 2hrs":
                                    blo=2
                                if mat=="Inglés Nivel Transicion (Prekinder y Kinder) - 1hr":
                                    blo=1
                                if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                    blo=2
                                if mat=="Asignatura Kinder - 1hr":
                                    blo=1
                            else:
                                if mat=="Asignatura PreKinder - 1hr":
                                    blo=1
                                if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                    blo=2
                                if mat=="Inglés Nivel Transicion (Prekinder y Kinder) - 1hr":
                                    blo=1
                                if mat=="Religión (Todas) - 2hrs":
                                    blo=2
                            if blo == 0:
                                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                                cur=Curso.objects.all()
                                datos={"r2":'La asignatura no es válida para el curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                                return render(request,'registrar_asignatura.html',datos)

                            cur=str(cur)
                            a.nombre=mat
                            a.nivel=niv
                            a.bloque=blo
                            a.curso_id=cur
                            a.save()
                            h=Horario.objects.filter(asignatura_id=id)

                            des="Modificacion de Asignatura "+str(cod)+""
                            tabla="Asignatura"
                            fyh=datetime.now()
                            usuario=request.session.get("idUsuario")
                            his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                            his.save()
                            asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                            cur=Curso.objects.all()
                            datos={"r":'Asignatura modificada Correctamente!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                            return render(request,'registrar_asignatura.html',datos)        
                        else:
                            niv="MEDIA"
                            if cur==9 or cur==10:
                                if mat=="Lengua y Literatura (7mo a 2do Medio) - 6hrs":
                                    blo=6
                                if mat=="Matemática  (1ero Basico a 2do Medio) - 6hrs":
                                    blo=6
                                if mat=="Historia, Geografía y Ciencias Sociales  (5to a 2do Medio) - 4hrs":
                                    blo=4
                                if mat=="Artes Visuales o Música (1ero y 2do Medio) - 2hrs":
                                    blo=2
                                if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                    blo=2
                                if mat=="Orientación  (5to a 2do Medio) - 1hr":
                                    blo=1
                                if mat=="Tecnología  (5to a 2do Medio) - 1hr":
                                    blo=1
                                if mat=="Religión (Todas) - 2hrs":
                                    blo=2
                                if mat=="Idioma Extranjero: Inglés  (5to a 2do medio) - 3hrs":
                                    blo=3
                                if mat=="Ciencias Naturales  (1ero y 2do Medio) - 6hrs":
                                    blo=6
                            if cur==11 or cur==12:
                                if mat=="Lengua y Literatura (3ero y 4to Medio) - 3hrs":
                                    blo=3
                                if mat=="Matemática  (3ero y 4to Medio) - 3hrs":
                                    blo=3
                                if mat=="Historia, Geografía y Ciencias Sociales (3ero y 4to Medio) - 2hrs":
                                    blo=2
                                if mat=="Artes (3ero y 4to Medio) - 2hrs":
                                    blo=2
                                if mat=="Educación Física y Salud  (Todas) - 2hrs":
                                    blo=2
                                if mat=="Ciencias para la Ciudadanía (3ero y 4to Medio) - 2hrs":
                                    blo=2
                                if mat=="Religión (Todas) - 2hrs":
                                    blo=2
                                if mat=="Inglés (3ero y 4to Medio) - 2hrs":
                                    blo=2
                                if mat=="Filosofía (3ero y 4to Medio) - 2hrs":
                                    blo=2
                                if mat=="Electivo de lengua y literatura (3ero y 4to Medio) - 6hrs":
                                    blo=6
                                if mat=="Electivo de historia (3ero y 4to Medio) - 6hrs":
                                    blo=6
                                if mat=="Electivo de matematicas (3ero y 4to Medio) - 6hrs":
                                    blo=6
                                if mat=="Electivo de biología (3ero y 4to Medio) - 6hrs":
                                    blo=6
                                if mat=="Educación Ciudadana (3ero y 4to Medio) - 2hrs":
                                    blo=2
                                if mat=="Ciencias para la Ciudadanía (3ero y 4to Medio) - 2hrs":
                                    blo=2
                            h=Horario.objects.filter(asignatura_id=id)
                            if h:
                                j=0
                                for x in h:
                                    if x == h[j]:
                                        y=Horario.objects.get(id=h[j].id)
                                        y.profesor_id=""
                                        y.asignatura_id=""
                                        y.save()
                                    j=j+1

                            if blo == 0:
                                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                                cur=Curso.objects.all()
                                datos={"r2":'La asignatura no es válida para el curso seleccionado!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                                return render(request,'registrar_asignatura.html',datos)

                            cur=str(cur)
                            a.nombre=mat
                            a.nivel=niv
                            a.bloque=blo
                            a.curso_id=cur
                            a.save()

                            des="Modificacion de Asignatura "+str(cod)+""
                            tabla="Asignatura"
                            fyh=datetime.now()
                            usuario=request.session.get("idUsuario")
                            his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                            his.save()
                            asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                            cur=Curso.objects.all()
                            datos={"r":'Asignatura modificada Correctamente!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                            return render(request,'registrar_asignatura.html',datos)
            else:
                asg=Asignatura.objects.select_related("curso").all().order_by("curso_id")
                cur=Curso.objects.all()
                datos={"r2":'Error al realizar la modificacion!!',"cur":cur,"asg":asg,"nomUsuario":nomUsuario}
                return render(request,'registrar_asignatura.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#--------------Profesores--------------------------------------------------------
def mostrarRegistrarPro(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            pro=Profesor.objects.all().order_by("rut")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro}
            return render(request,'registrar_profesor.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------------
def mostrarModificarPro(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            id=Profesor.decode_hash(hash_id)
            rs=Profesor.objects.filter(id=id)
            if rs:
                pro=Profesor.objects.all().order_by("rut")
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"rs":rs}
                return render(request,'modificar_profesor.html',datos)
            else:
                pro=Profesor.objects.all().order_by("rut")
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"r2":'Profesor no disponible!!'}
                return render(request,'registrar_profesor.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#---------------------------------------------------------------------------
def registrarProfesor(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            if request.method=="POST":
                rut=request.POST["txtrut"]
                nom=request.POST["txtnom"]
                ape=request.POST["txtape"]
                niv=request.POST["opniv"]
                ema=request.POST["txtema"]
                comprobarProfesor=Profesor.objects.filter(rut=rut)
                if comprobarProfesor:
                    pro=Profesor.objects.all().order_by("rut")
                    datos={"r2":'Profesor ya registrado',"pro":pro,"nomUsuario":nomUsuario,"cargo":cargoUsuario}
                    return render(request,'registrar_profesor.html',datos)
                else:
                    n=Profesor.objects.count()+1
                    for x in range(1,n+1):
                        m=Profesor.objects.filter(id=x)
                        if m=="":
                            n=x
                            break
                    p=Profesor(id=n,rut=rut,nombre=nom,apellido=ape,nivel=niv)
                    p.save()

                    des="Registro de Profesor "+str(rut)+""
                    tabla="Profesor"
                    fyh=datetime.now()
                    usuario=request.session.get("idUsuario")
                    his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                    his.save()
                    
                    comprobarUsuario=User.objects.filter(email=ema)
                    if comprobarUsuario:
                        pro=Profesor.objects.all().order_by("rut")
                        datos={"r2":'Email ya registrado',"pro":pro,"nomUsuario":nomUsuario,"cargo":cargoUsuario}
                        return render(request,'registrar_profesor.html',datos)
                    else:
                        user = User.objects.create_user(
                            username=ema,
                            password=rut,
                            email=ema,
                            is_staff=True,
                            is_superuser=False
                        )
                        user.save()
                        Usuario.objects.create(
                            nombre=ema,
                            password=rut,
                            cargo="PROFESOR",
                            user=user
                        )

                    pro=Profesor.objects.all().order_by("rut")
                    datos={"r":'Profesor registrado correctamente',"pro":pro,"nomUsuario":nomUsuario,"cargo":cargoUsuario}
                    return render(request,'registrar_profesor.html',datos)
            else:
                pro=Profesor.objects.all().order_by("rut")
                datos={"r2":'No se pudo ejecutar la solicitud',"pro":pro,"nomUsuario":nomUsuario,"cargo":cargoUsuario}
                return render(request,'registrar_profesor.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------------------
def modificarProfesor(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            if request.method=="POST":
                rut=request.POST["txtrut"]
                nom=request.POST["txtnom"]
                ape=request.POST["txtape"]
                ema=request.POST.get("txtema", "")
                niv=request.POST["opniv"]
                id=Profesor.decode_hash(hash_id)
                comprobarRut=Profesor.objects.filter(rut=rut)
                if comprobarRut:
                    RutID=Profesor.objects.filter(id=id,rut=rut)
                    if RutID:
                        p=Profesor.objects.get(id=id)
                        if p.nivel==niv:
                            p=Profesor.objects.get(id=id)
                            p.nombre=nom
                            p.apellido=ape
                            p.email=ema or p.email
                            p.save()
                        else:
                            p=Profesor.objects.get(id=id)
                            p.nombre=nom
                            p.apellido=ape
                            p.email=ema or p.email
                            p.nivel=niv
                            p.save()

                            h=Horario.objects.filter(profesor_id=id)
                            if h:
                                j=0
                                for x in h:
                                    if x == h[j]:
                                        y=Horario.objects.get(id=h[j].id)
                                        y.profesor_id=""
                                        y.asignatura_id=""
                                        y.save()

                                    j=j+1

                        des="Modificacion de Profesor "+str(rut)+""
                        tabla="Profesor"
                        fyh=datetime.now()
                        usuario=request.session.get("idUsuario")
                        his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                        his.save()
                        pro=Profesor.objects.all().order_by("rut")
                        datos={"r":'Datos Modificados correctamente!!',"pro":pro,"nomUsuario":nomUsuario}
                        return render(request,'registrar_profesor.html',datos)
                    else:
                        pro=Profesor.objects.all().order_by("rut")
                        datos={"r2":'El rut indicado ya esta en uso!!',"pro":pro,"nomUsuario":nomUsuario}
                        return render(request,'modificar_profesor.html',datos)
                else:
                    p=Profesor.objects.get(id=id)
                    if p.nivel==niv:
                        p=Profesor.objects.get(id=id)
                        p.rut=rut
                        p.nombre=nom
                        p.apellido=ape
                        p.email=ema or p.email
                        p.save()
                    else:
                        p=Profesor.objects.get(id=id)
                        p.rut=rut
                        p.nombre=nom
                        p.apellido=ape
                        p.email=ema or p.email
                        p.nivel=niv
                        p.save()
                        h=Horario.objects.filter(profesor_id=id)
                        if h:
                            j=0
                            for x in h:
                                if x == h[j]:
                                    y=Horario.objects.get(id=h[j].id)
                                    y.profesor_id=""
                                    y.asignatura_id=""
                                    y.save()

                                j=j+1

                    des="Modificacion de Profesor "+str(rut)+""
                    tabla="Profesor"
                    fyh=datetime.now()
                    usuario=request.session.get("idUsuario")
                    his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                    his.save()
                    pro=Profesor.objects.all().order_by("rut")
                    datos={"r":'Datos Modificados correctamente',"pro":pro,"nomUsuario":nomUsuario}
                    return render(request,'registrar_profesor.html',datos)
            else:
                pro=Profesor.objects.all().order_by("rut")
                datos={"r2":'Error al realizar la consulta!!',"pro":pro,"nomUsuario":nomUsuario}
                return render(request,'registrar_profesor.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#---------------------------------------------------------------------------
def eliminarProfesor(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            id=Profesor.decode_hash(hash_id)
            pro=Profesor.objects.filter(id=id)
            if pro:
                p=Profesor.objects.get(id=id)
                rut=p.rut

                h=Horario.objects.filter(profesor_id=id)
                if h:
                    j=0
                    for x in h:
                        if x == h[j]:
                            y=Horario.objects.get(id=h[j].id)
                            y.profesor_id=""                                                                                  #Eliminacion de Profesores
                            y.asignatura_id=""                                                                                #Metodo para no eliminar datos de tablas que se desean conservar
                            y.save()

                        j=j+1

                p.habilitado = False
                p.save()
                des="Eliminacion de Profesor "+str(rut)+""
                tabla="Profesor"
                fyh=datetime.now()
                usuario=request.session.get("idUsuario")
                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                his.save()
                pro=Profesor.objects.filter(habilitado=True).order_by("rut")
                datos={"r":'Profesor eliminado Correctamente!!',"pro":pro,"nomUsuario":nomUsuario}
                return render(request,'registrar_profesor.html',datos)
            else:
                pro=Profesor.objects.filter(habilitado=True).order_by("rut")
                datos={"r2":'El Profesor no se pudo eliminar!!',"pro":pro,"nomUsuario":nomUsuario}
                return render(request,'registrar_profesor.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#----------------Horarios----------------------------------------------------------------
def mostrarRegistrarHor(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
            dis=DisponibilidadProfesor.objects.all().values()
            cur=Curso.objects.all().order_by("id")
            pro=Profesor.objects.all().order_by("rut")
            hor=Horario.objects.select_related("curso","asignatura","profesor").all().order_by("curso_id","dia")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"asg":asg,"pro":pro,"hor":hor,"dis":dis}
            return render(request,'registrar_horarios.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#---------------------------------------------------------------------------------------
def mostrarHorario(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            idc=Curso.decode_hash(hash_id)
            pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count')[:1],
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
            asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
            dias=["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES"]
            for b in range(1,10):
                for d in dias:
                    if not Horario.objects.filter(curso_id=idc,bloque=b,dia=d).exists():
                        Horario.objects.create(curso_id=idc,bloque=b,dia=d)
            hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=idc)
            hor2=Horario.objects.all().values()
            asgpro=AsignaturasProfesor.objects.select_related("asignartura","profesor")

            query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            query2 = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
            with connection.cursor() as cursor:
                cursor.execute(query2)
                results2 = cursor.fetchall()

            full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]

            datos = {"nomUsuario":nomUsuario,"cargo":cargoUsuario,"asg":asg,"hor":hor,"pro2":pro2,"idc":idc, "hor2":hor2, "asgpro":asgpro, "results": results, "results2": results2, "full_asg_ids": full_asg_ids}

            return render(request, 'modificar_horario.html', datos)

        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#---------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def cambiarHorario(request,id, idc):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            if request.method=="POST":
                if 'btnguardar' in request.POST:
                        h=Horario.objects.get(id=id)
                        asi=request.POST["opasg"]
                        pr=request.POST["oppro"]
                        dia=h.dia
                        bl=h.bloque
                        id2=h.curso_id
                        rp=h.profesor_id
                        id2=int(id2)
                        comprobarDis=DisponibilidadProfesor.objects.filter(profesor_id=pr,dia=dia,bloque=bl,estado="DISPONIBLE")
                        if comprobarDis:
                            asgi=Asignatura.objects.get(id=asi)
                            blo=asgi.bloques                                                         #Modificacion y/o Registro de Horarios
                            nv=asgi.nivel
                            nom=asgi.nombre
                            comprobarAsi=Horario.objects.filter(asignatura_id=asi,curso_id=id2)
                            if len(comprobarAsi)==blo:
                                j=0
                                for i in comprobarAsi:
                                    if id == comprobarAsi[j].id:
                                        comprobarEsp=AsignaturasProfesor.objects.filter(nombre=nom,nivel=nv,profesor_id=pr)
                                        if comprobarEsp:
                                            ho=Horario.objects.filter(profesor_id=pr,bloque=bl,dia=dia)
                                            if ho:
                                                # ho=Horario.objects.get(profesor_id=pr,bloque=bl,dia=dia)
                                                if ho.filter(curso_id=id2).exists():
                                                    h=Horario.objects.get(id=id)
                                                    h.profesor_id=pr
                                                    h.save()

                                                    c=Curso.objects.get(id=id2)
                                                    cu=c.nombre
                                                    des="Modificacion de Horario "+str(cu)+""
                                                    tabla="Horario"
                                                    fyh=datetime.now()
                                                    usuario=request.session.get("idUsuario")
                                                    his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                                    his.save()

                                                    pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count')[:1],
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                                    asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                                    hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                                    hor2=Horario.objects.all().values()

                                                    query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                                    with connection.cursor() as cursor:
                                                        cursor.execute(query)
                                                        results = cursor.fetchall()



                                                    query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                                    with connection.cursor() as cursor:
                                                        cursor.execute(query)
                                                        results2 = cursor.fetchall()

                                                    full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                                    datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2, "results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r":'Horario Modificado Correctamente!!',"idc":idc, "hor2":hor2}
                                                    return render(request,'modificar_horario.html',datos)
                                                else:
                                                    pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count')[:1],
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                                    asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                                    hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                                    hor2=Horario.objects.all().values()

                                                    query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                                    with connection.cursor() as cursor:
                                                        cursor.execute(query)
                                                        results = cursor.fetchall()

                                                    query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                                    with connection.cursor() as cursor:
                                                        cursor.execute(query)
                                                        results2 = cursor.fetchall()


                                                    full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                                    datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2, "results": results,"results2": results2, "full_asg_ids": full_asg_ids, "r2":'Profesor ya tomo una clase en el bloque seleccionado!!',"idc":idc, "hor2":hor2}
                                                    return render(request,'modificar_horario.html',datos)
                                            else:
                                                h=Horario.objects.get(id=id)
                                                h.profesor_id=pr
                                                h.save()

                                                c=Curso.objects.get(id=id2)
                                                cu=c.nombre
                                                des="Modificacion de Horario "+str(cu)+""
                                                tabla="Horario"
                                                fyh=datetime.now()
                                                usuario=request.session.get("idUsuario")
                                                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                                his.save()

                                                pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                                asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                                hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                                hor2=Horario.objects.all().values()

                                                query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                                with connection.cursor() as cursor:
                                                    cursor.execute(query)
                                                    results = cursor.fetchall()


                                                query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                                with connection.cursor() as cursor:
                                                    cursor.execute(query)
                                                    results2 = cursor.fetchall()


                                                full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                                datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results,"results2": results2, "full_asg_ids": full_asg_ids, "r":'Horario Modificado Correctamente!!',"idc":idc, "hor2":hor2}

                                                return render(request,'modificar_horario.html',datos)
                                    j=j+1

                                pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                hor2=Horario.objects.all().values()

                                query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                with connection.cursor() as cursor:
                                    cursor.execute(query)
                                    results = cursor.fetchall()


                                query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                with connection.cursor() as cursor:
                                    cursor.execute(query)
                                    results2 = cursor.fetchall()



                                full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r2":'No se puede agregar mas bloques de esta Asignatura en el Curso Seleccionado!!',"idc":idc, "hor2":hor2}
                                return render(request,'modificar_horario.html',datos)
                            else:
                                comprobarEsp=AsignaturasProfesor.objects.filter(nombre=nom,profesor_id=pr)
                                if comprobarEsp:
                                    ho=Horario.objects.filter(profesor_id=pr,bloque=bl,dia=dia)
                                    if ho:
                                        # hor=Horario.objects.get(profesor_id=pr,bloque=bl,dia=dia)
                                        if ho.filter(curso_id=id2).exists():
                                            c=Curso.objects.get(id=id2)
                                            cu=c.nombre
                                            h=Horario.objects.get(id=id)
                                            h.asignatura_id=asi
                                            h.profesor_id=pr
                                            h.save()
                                            des="Modificacion de Horario "+str(cu)+""
                                            tabla="Horario"
                                            fyh=datetime.now()
                                            usuario=request.session.get("idUsuario")
                                            his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                            his.save()

                                            pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                            asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                            hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                            hor2=Horario.objects.all().values()

                                            query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                            with connection.cursor() as cursor:
                                                cursor.execute(query)
                                                results = cursor.fetchall()


                                            query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                            with connection.cursor() as cursor:
                                                cursor.execute(query)
                                                results2 = cursor.fetchall()



                                            full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                            datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r":'Horario Modificado Correctamente!!',"idc":idc, "hor2":hor2}

                                            return render(request,'modificar_horario.html',datos)
                                        else:
                                            p=0
                                            hor=Horario.objects.filter(profesor_id=pr,bloque=bl,dia=dia)
                                            for x in hor:
                                                p=p+1
                                            if p==1:
                                                c=Curso.objects.get(id=id2)
                                                cu=c.nombre
                                                h=Horario.objects.get(id=id)
                                                h.asignatura_id=asi
                                                h.profesor_id=pr
                                                h.save()
                                                des="Modificacion de Horario "+str(cu)+""
                                                tabla="Horario"
                                                fyh=datetime.now()
                                                usuario=request.session.get("idUsuario")
                                                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                                his.save()

                                                pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")

                                                asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                                hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                                hor2=Horario.objects.all().values()

                                                query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                                with connection.cursor() as cursor:
                                                    cursor.execute(query)
                                                    results = cursor.fetchall()


                                                query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                                with connection.cursor() as cursor:
                                                    cursor.execute(query)
                                                    results2 = cursor.fetchall()



                                                full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                                datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r":'Horario Modificado Correctamente!!',"idc":idc, "hor2":hor2}
                                                return render(request,'modificar_horario.html',datos)
                                            else:
                                                if id2==1 or id2==2 or id2==3 or id2==4 or id2==5 or id2==6 or id2==7 or id2==8:
                                                    pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                                else:
                                                    pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                                                asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                                hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                                hor2=Horario.objects.all().values()

                                                query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                                with connection.cursor() as cursor:
                                                    cursor.execute(query)
                                                    results = cursor.fetchall()

                                                query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                                with connection.cursor() as cursor:
                                                    cursor.execute(query)
                                                    results2 = cursor.fetchall()




                                                full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                                datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r2":'Profesor ya tomo una clase en el bloque seleccionado!!',"idc":idc, "hor2":hor2}
                                                return render(request,'modificar_horario.html',datos)
                                    else:
                                        c=Curso.objects.get(id=id2)
                                        cu=c.nombre
                                        h=Horario.objects.get(id=id)
                                        h.asignatura_id=asi
                                        h.profesor_id=pr
                                        h.save()
                                        des="Modificacion de Horario "+str(cu)+""
                                        tabla="Horario"
                                        fyh=datetime.now()
                                        usuario=request.session.get("idUsuario")
                                        his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                                        his.save()

                                        pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")

                                        asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                        hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                        hor2=Horario.objects.all().values()

                                        query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                        with connection.cursor() as cursor:
                                            cursor.execute(query)
                                            results = cursor.fetchall()


                                        query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                        with connection.cursor() as cursor:
                                            cursor.execute(query)
                                            results2 = cursor.fetchall()



                                        full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                        datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r":'Horario Modificado Correctamente!!',"idc":idc, "hor2":hor2}
                                        return render(request,'modificar_horario.html',datos)
                                else:
                                    pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")

                                    asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                                    hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                                    hor2=Horario.objects.all().values()

                                    query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                                    with connection.cursor() as cursor:
                                        cursor.execute(query)
                                        results = cursor.fetchall()

                                    query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                                    with connection.cursor() as cursor:
                                            cursor.execute(query)
                                            results2 = cursor.fetchall()



                                    full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                                    datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r2":'Profesor no capacitado para dictar la Asignatura Seleccionada!!',"idc":idc, "hor2":hor2}
                                    return render(request,'modificar_horario.html',datos)
                        else:
                            pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")

                            asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                            hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                            hor2=Horario.objects.all().values()

                            query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                            with connection.cursor() as cursor:
                                cursor.execute(query)
                                results = cursor.fetchall()

                            query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                            with connection.cursor() as cursor:
                                    cursor.execute(query)
                                    results2 = cursor.fetchall()




                            full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                            datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r2":'Profesor no Disponible para dar clase en este Bloque!!',"idc":idc, "hor2":hor2}
                            return render(request,'modificar_horario.html',datos)


                if 'btnquitar' in request.POST:

                    h=Horario.objects.get(id=id)
                    h.asignatura_id=None
                    h.profesor_id=None
                    h.save()
                    #des="Modificacion de Horario "+str(cu)+""
                    #tabla="Horario"
                    #fyh=datetime.now()
                    #usuario=request.session.get("idUsuario")
                    #his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                    #his.save()

                    pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")
                    asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                    hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=idc)
                    hor2=Horario.objects.all().values()

                    query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                    with connection.cursor() as cursor:
                        cursor.execute(query)
                        results = cursor.fetchall()

                    query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                    with connection.cursor() as cursor:
                            cursor.execute(query)
                            results2 = cursor.fetchall()




                    full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                    datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r":'Horario Quitado Correctamente!!',"idc":idc, "hor2":hor2}
                    return render(request,'modificar_horario.html',datos)





            else:
                h=Horario.objects.get(id=id)
                id2=h.curso_id
                pro2 = DisponibilidadProfesor.objects.select_related("profesor").filter(
    estado="DISPONIBLE"
).annotate(
    clases_ocupadas=Coalesce(
        Subquery(
            Horario.objects.filter(
                profesor_id=OuterRef('profesor_id'),
                dia=OuterRef('dia'),
                bloque=OuterRef('bloque')
            ).values('profesor_id').annotate(count=Count('id')).values('count'),
            output_field=IntegerField()
        ), 0
    )
).order_by("profesor__nombre")

                asg=Asignatura.objects.select_related("curso").all().order_by("nombre")
                hor=Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=id2)
                hor2=Horario.objects.all().values()

                query = "select distinct horarios_profesor.* from horarios_profesor inner join horarios_horario on horarios_horario.profesor_id = horarios_profesor.id where horarios_horario.curso_id='" + str(idc) + "'"

                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()

                query = "select horarios_asignatura.codigo, horarios_asignatura.id, horarios_asignatura.nombre, horarios_asignatura.bloques, count(horarios_horario.asignatura_id) as cantidad, horarios_horario.curso_id  from horarios_asignatura, horarios_horario where horarios_asignatura.curso_id='" + str(idc) + "' and horarios_asignatura.id=horarios_horario.asignatura_id group by horarios_asignatura.id"
                with connection.cursor() as cursor:
                        cursor.execute(query)
                        results2 = cursor.fetchall()



                full_asg_ids = [row[1] for row in results2 if row[5] == idc and row[4] >= row[3]]
                datos={"nomUsuario":nomUsuario,"asg":asg,"hor":hor,"pro2":pro2,"results": results, "results2": results2, "full_asg_ids": full_asg_ids, "r2":'Debe Presionar el Boton para Continuar!!',"idc":idc, "hor2":hor2}
                return render(request,'modificar_horario.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#---------------------------------------------------------------------------------
@role_required(['DIRECTOR', 'PROFESOR', 'ADMINISTRADOR', 'ESTUDIANTE', 'ALUMNO'])
def mostrarVisualizarHorario(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        cur=Curso.objects.all().order_by("id")
        if cargoUsuario=="PROFESOR":
            idAuthUser=request.session.get("idAuthUser")
            datpro=Profesor.objects.filter(usuario_id=idAuthUser).values()
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"datpro":datpro}
        elif cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
            idAuthUser=request.session.get("idAuthUser")
            datest=Alumnos.objects.filter(user_id=idAuthUser).values()
            # Cargar horario automáticamente del curso del alumno
            hor=None
            try:
                if datest:
                    nombre_curso = datest[0]["curso"]
                    curso_obj = Curso.objects.filter(nombre=nombre_curso).first()
                    if curso_obj:
                        hor = Horario.objects.select_related("curso","asignatura","profesor").filter(curso_id=curso_obj.id)
            except Exception:
                hor=None
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"datest":datest,"hor":hor}
        else:
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur}
        return render(request,'visualizar_horarios.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#--------------------------------------------------------------------------------
def buscarCurso(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if request.method=="POST":
            # Si es estudiante/alumno, forzar su propio curso
            if cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
                idAuthUser=request.session.get("idAuthUser")
                datest=Alumnos.objects.filter(user_id=idAuthUser).values()
                if datest:
                    nombre_curso = datest[0]["curso"]
                    c=Curso.objects.filter(nombre=nombre_curso)
                    id = c[0].id if c else None
                else:
                    id = None
            else:
                id=request.POST["opcur"]
            c=Curso.objects.filter(id=id)
            if c:
                comprobarHor=Horario.objects.filter(curso_id=id)
                if comprobarHor:
                    hor=Horario.objects.select_related("curso").filter(curso_id=id)
                    cur=Curso.objects.all().order_by("id")
                    if cargoUsuario=="PROFESOR":
                        datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"hor":hor,"r":'El Curso posee horario registrado!!',"datpro":datpro}
                    elif cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
                        datest=Alumnos.objects.filter(email=nomUsuario.lower()).values()
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"hor":hor,"r":'El Curso posee horario registrado!!',"datest":datest}
                    else:
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"hor":hor,"r":'El Curso posee horario registrado!!'}
                    return render(request,'visualizar_horarios.html',datos)
                else:
                    cur=Curso.objects.all().order_by("id")
                    if cargoUsuario=="PROFESOR":
                        datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r3":'El Curso no posee Horario Registrado!!',"datpro":datpro}
                    elif cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
                        datest=Alumnos.objects.filter(email=nomUsuario.lower()).values()
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r3":'El Curso no posee Horario Registrado!!',"datest":datest}
                    else:
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r3":'El Curso no posee Horario Registrado!!'}
                    return render(request,'visualizar_horarios.html',datos)
            else:
                cur=Curso.objects.all().order_by("id")
                if cargoUsuario=="PROFESOR":
                    datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r2":'Curso no Registrado!!',"datpro":datpro}
                elif cargoUsuario=="ESTUDIANTE" or cargoUsuario=="ALUMNO":
                    datest=Alumnos.objects.filter(email=nomUsuario.lower()).values()
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r2":'Curso no Registrado!!',"datest":datest}
                else:
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r2":'Curso no Registrado!!'}
                return render(request,'visualizar_horarios.html',datos)
        else:
            cur=Curso.objects.all().order_by("id")
            if cargoUsuario=="PROFESOR":
                datpro=Profesor.objects.filter(email=nomUsuario.lower()).values()
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r2":'Debe Presionar el Boton de Busqueda!!',"datpro":datpro}
            elif cargoUsuario=="ESTUDIANTE":
                datest=Alumnos.objects.filter(email=nomUsuario.lower()).values()
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r2":'Debe Presionar el Boton de Busqueda!!',"datest":datest}
            else:
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"cur":cur,"r2":'Debe Presionar el Boton de Busqueda!!'}
            return render(request,'visualizar_horarios.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#----------------------------------------------------------------------------------------------
#----------------Disponibilidad-----------------------------------------------------------------
@role_required(['DIRECTOR', 'PROFESOR', 'ADMINISTRADOR'])
@profesor_data_only
def mostrarVisualizarDisp(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="PROFESOR":
            idAuthUser=request.session.get("idAuthUser") or request.session.get("idUsuario")
            p_req=getattr(request, "profesor_actual", None)
            email=(nomUsuario or "").lower()
            idp = (
                p_req
                or Profesor.objects.filter(usuario_id=idAuthUser).first()
                or Profesor.objects.filter(email__iexact=email).first()
                or (getattr(request, "user", None) and request.user.is_authenticated and Profesor.objects.filter(usuario_id=request.user.id).first())
            )
            datpro = Profesor.objects.filter(id=idp.id).values() if idp else []
            bloques = [1,2,3,4,5,6,7,8,9]
            dias = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES"]
            base = {(b,d):"NO DISPONIBLE" for b in bloques for d in dias}
            if idp:
                dis_qs = list(DisponibilidadProfesor.objects.filter(profesor_id=idp.id).values("bloque","dia","estado"))
                for d in dis_qs:
                    base[(d["bloque"], d["dia"])]=d["estado"]
                hor_occ = Horario.objects.filter(profesor_id=idp.id, asignatura_id__isnull=False).values("bloque","dia")
                for h in hor_occ:
                    k=(h["bloque"], h["dia"]) 
                    base[k] = "DISPONIBLE"
            dis = [{"bloque":b,"dia":d,"estado":base[(b,d)]} for b in bloques for d in dias]
            pro=Profesor.objects.all().order_by("rut")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"dis":dis, "datpro":datpro, "pro":pro}
            return render(request,'visualizar_disponibilidad.html',datos)
        else:
            pro=Profesor.objects.all().order_by("rut")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro}
            return render(request,'visualizar_disponibilidad.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#---------------------------------------------------------------------------------
def mostrarRegistrarDis(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            id=Profesor.decode_hash(hash_id)
            rs=Profesor.objects.filter(id=id)
            if rs:
                dis=DisponibilidadProfesor.objects.filter(profesor_id=id)
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"dis":dis}
                return render(request,'registrar_disponibilidad.html',datos)
            else:
                pro=Profesor.objects.all().order_by("rut")
                datos={"r2":'Profesor no registrado!!',"pro":pro,"nomUsuario":nomUsuario,"cargo":cargoUsuario}
                return render(request,'registrar_profesor.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#----------------------------------------------------------------------------------
def buscarProfesorDis(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        id=Profesor.decode_hash(hash_id)
        p=Profesor.objects.filter(id=id)
        if p:
            comprobarDis=DisponibilidadProfesor.objects.filter(profesor_id=id)
            if comprobarDis:
                comprobarHor=Horario.objects.filter(profesor_id=id)
                if comprobarHor:
                    hor=Horario.objects.select_related("profesor").filter(profesor_id=id).order_by("curso_id")
                    lun1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=1).order_by("curso_id")
                    lun2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=2).order_by("curso_id")
                    lun3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=3).order_by("curso_id")
                    lun4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=4).order_by("curso_id")
                    lun5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=5).order_by("curso_id")
                    lun6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=6).order_by("curso_id")
                    lun7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=7).order_by("curso_id")
                    lun8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=8).order_by("curso_id")
                    lun9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=9).order_by("curso_id")
                    mar1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=1).order_by("curso_id")
                    mar2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=2).order_by("curso_id")
                    mar3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=3).order_by("curso_id")
                    mar4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=4).order_by("curso_id")
                    mar5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=5).order_by("curso_id")
                    mar6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=6).order_by("curso_id")
                    mar7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=7).order_by("curso_id")
                    mar8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=8).order_by("curso_id")
                    mar9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=9).order_by("curso_id")
                    mie1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=1).order_by("curso_id")
                    mie2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=2).order_by("curso_id")
                    mie3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=3).order_by("curso_id")
                    mie4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=4).order_by("curso_id")
                    mie5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=5).order_by("curso_id")
                    mie6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=6).order_by("curso_id")
                    mie7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=7).order_by("curso_id")
                    mie8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=8).order_by("curso_id")
                    mie9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=9).order_by("curso_id")
                    jue1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=1).order_by("curso_id")
                    jue2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=2).order_by("curso_id")
                    jue3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=3).order_by("curso_id")
                    jue4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=4).order_by("curso_id")
                    jue5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=5).order_by("curso_id")
                    jue6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=6).order_by("curso_id")
                    jue7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=7).order_by("curso_id")
                    jue8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=8).order_by("curso_id")
                    jue9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=9).order_by("curso_id")
                    vie1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=1).order_by("curso_id")
                    vie2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=2).order_by("curso_id")
                    vie3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=3).order_by("curso_id")
                    vie4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=4).order_by("curso_id")
                    vie5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=5).order_by("curso_id")
                    vie6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=6).order_by("curso_id")
                    vie7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=7).order_by("curso_id")
                    vie8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=8).order_by("curso_id")
                    vie9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=9).order_by("curso_id")
                    dis_qs=DisponibilidadProfesor.objects.select_related("profesor").filter(profesor_id=id)
                    rs=Profesor.objects.filter(id=id)
                    pro=Profesor.objects.all().order_by("rut")
                    hor_occ=Horario.objects.filter(profesor_id=id, asignatura_id__isnull=False).values("bloque","dia")
                    occ={(h["bloque"], h["dia"]) for h in hor_occ}
                    dis=list(dis_qs.values("bloque","dia","estado"))
                    dis=[{"bloque":d["bloque"],"dia":d["dia"],"estado":"DISPONIBLE" if (d["bloque"],d["dia"]) in occ else d["estado"]} for d in dis]
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"dis":dis,"rs":rs,"r":'El Profesor Posee Disponibilidad Registrada!!',
                           "lun1":lun1,"lun2":lun2,"lun3":lun3,"lun4":lun4,"lun5":lun5,"lun6":lun6,"lun7":lun7,"lun8":lun8,"lun9":lun9,
                           "mar1":mar1,"mar2":mar2,"mar3":mar3,"mar4":mar4,"mar5":mar5,"mar6":mar6,"mar7":mar7,"mar8":mar8,"mar9":mar9,
                           "mie1":mie1,"mie2":mie2,"mie3":mie3,"mie4":mie4,"mie5":mie5,"mie6":mie6,"mie7":mie7,"mie8":mie8,"mie9":mie9,
                           "jue1":jue1,"jue2":jue2,"jue3":jue3,"jue4":jue4,"jue5":jue5,"jue6":jue6,"jue7":jue7,"jue8":jue8,"jue9":jue9,
                           "vie1":vie1,"vie2":vie2,"vie3":vie3,"vie4":vie4,"vie5":vie5,"vie6":vie6,"vie7":vie7,"vie8":vie8,"vie9":vie9,
                           "hor":hor}
                    return render(request,'visualizar_disponibilidad.html',datos)
                else:
                    dis=DisponibilidadProfesor.objects.select_related("profesor").filter(profesor_id=id)
                    rs=Profesor.objects.filter(id=id)
                    pro=Profesor.objects.all().order_by("rut")
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"dis":dis,"rs":rs,"r":'El Profesor Posee Disponibilidad Registrada!!'}
                    return render(request,'visualizar_disponibilidad.html',datos)
            else:
                pro=Profesor.objects.all().order_by("rut")
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"r3":'El Profesor no Posee Disponibilidad Registrada!!'}
                return render(request,'visualizar_disponibilidad.html',datos)
        else:
            pro=Profesor.objects.all().order_by("rut")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"r2":'Profesor no Registrado!!'}
            return render(request,'visualizar_disponibilidad.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------------------------------
def cambiarDisponibilidad(request,id,id2):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            dis=DisponibilidadProfesor.objects.filter(id=id)
            if dis:
                d=DisponibilidadProfesor.objects.get(id=id)
                dia=d.dia
                es=d.estado
                bl=d.bloque
                if es == "NO DISPONIBLE":
                    d.estado="DISPONIBLE"
                    est="DISPONIBLE"
                else:
                    d.estado="NO DISPONIBLE"
                    est="NO DISPONIBLE"
                    h=Horario.objects.filter(profesor_id=id2,bloque=bl)                          #Registro de Disponibilidad
                    if h:                                                                                #Metodo para alterar los Horarios sin eliminar datos que se desean conservar
                        j=0
                        for x in h:
                            if x == h[j]:
                                y=Horario.objects.get(id=h[j].id)
                                y.profesor_id=""
                                y.asignatura_id=""
                                y.save()

                            j=j+1
                d.save()
                p=Profesor.objects.get(id=id2)
                pr=p.rut
                des="Cambio de Disponibilidad ("+str(dia)+") estado ("+str(est)+") de Profesor "+str(pr)+""
                tabla="DisponibilidadProfesor"
                fyh=datetime.now()
                usuario=request.session.get("idUsuario")
                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                his.save()
                rs=Profesor.objects.filter(id=id2)
                dis=DisponibilidadProfesor.objects.filter(profesor_id=id2)
                datos={"nomUsuario":nomUsuario,"rs":rs,"dis":dis,"r":'Disponibilidad Modificada Correctamente!!'}
                return render(request, 'registrar_disponibilidad.html',datos)
            else:
                rs=Profesor.objects.filter(id=id2)
                dis=DisponibilidadProfesor.objects.filter(profesor_id=id2)
                datos={"nomUsuario":nomUsuario,"rs":rs,"dis":dis,"r2":'Debe Seleccionar un Bloque para Modifiacar!!'}
                return render(request, 'registrar_especialidad.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-----------------------Especialidades del Profesor-------------------------
def mostrarRegistrarEsp(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            id=Profesor.decode_hash(hash_id)
            rs=Profesor.objects.filter(id=id)
            esp=AsignaturasProfesor.objects.filter(profesor_id=id)
            asi=Asignatura.objects.all().values()
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"esp":esp,"asi":asi}
            return render(request, 'registrar_especialidad.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------------------------------
def registrarEspecialidad(request,hash_id):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            if request.method=="POST":
                    id=Profesor.decode_hash(hash_id)
                    asg=request.POST["opasg"]
                    niv='BASICA y MEDIA'
                    es=AsignaturasProfesor.objects.filter(nombre=asg,profesor_id=id,nivel=niv)
                    if es:
                        rs=Profesor.objects.filter(id=id)
                        esp=AsignaturasProfesor.objects.filter(profesor_id=id)
                        asi=Asignatura.objects.all().values()
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"asi":asi,"esp":esp,"r2":'La Especialidad "'+str(asg)+' ('+str(niv)+')" ya esta Registrada!!'}
                        return render(request, 'registrar_especialidad.html',datos)
                    else:
                        e=AsignaturasProfesor(nombre=asg,nivel=niv,profesor_id=id)
                        e.save()
                        p=Profesor.objects.get(id=id)
                        pr=p.rut
                        des="Registro de Especialidad "+str(pr)+""
                        tabla="AsignaturasProfesor"
                        fyh=datetime.now()
                        usuario=request.session.get("idUsuario")
                        his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                        his.save()
                        rs=Profesor.objects.filter(id=id)
                        esp=AsignaturasProfesor.objects.filter(profesor_id=id)
                        asi=Asignatura.objects.all().values()
                        datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"asi":asi,"esp":esp,"r":'Especialidades Registradas Correctamente!!'}
                        return render(request, 'registrar_especialidad.html',datos)
            else:
                rs=Profesor.objects.filter(id=id)
                esp=AsignaturasProfesor.objects.filter(profesor_id=id)
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"esp":esp,"r2":'Debe Presionar El Boton de Registro!!'}
                return render(request, 'registrar_especialidad.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-----------------------------------------------------------------------------
def eliminarEspecialidad(request,id,id2):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="ADMINISTRADOR":
            esp=AsignaturasProfesor.objects.filter(id=id)
            if esp:
                e=AsignaturasProfesor.objects.get(id=id)
                nom=e.nombre
                niv=e.nivel
                a=Asignatura.objects.filter(nombre=nom,nivel=niv)
                h=Horario.objects.filter(profesor_id=id2)
                if h and a:
                    j=0
                    for x in h:
                        if x == h[j] and h[j].asignatura_id == a[0].id:
                            y=Horario.objects.get(id=h[j].id)
                            y.profesor_id=""
                            y.asignatura_id=""
                            y.save()
                        j=j+1
                e.habilitado = False
                e.save()
                p=Profesor.objects.get(id=id2)
                pr=p.rut
                des="Eliminacion de Registro ("+str(nom)+") nivel ("+str(niv)+") de Profesor "+str(pr)+""
                tabla="AsignaturasProfesor"
                fyh=datetime.now()
                usuario=request.session.get("idUsuario")
                his=Historial(accion=des,tabla=tabla,fecha=fyh,usuario_id=usuario)
                his.save()
                rs=Profesor.objects.filter(id=id2)
                esp=AsignaturasProfesor.objects.filter(profesor_id=id2, habilitado=True)
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"esp":esp,"r":'Especialidad Eliminada Correctamente!!'}
                return render(request, 'registrar_especialidad.html',datos)
            else:
                rs=Profesor.objects.filter(id=id2)
                esp=AsignaturasProfesor.objects.filter(profesor_id=id2, habilitado=True)
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"rs":rs,"esp":esp,"r2":'Debe Seleccionar una Especialidad para Eliminar!!'}
                return render(request, 'registrar_especialidad.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#----------------------------Historial----------------------------------------------
def mostrarHistorial(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario=="DIRECTOR":
            his=Historial.objects.all().order_by("-fecha")
            datos={"his":his,"nomUsuario":nomUsuario,"cargo":cargoUsuario}
            return render(request,'listar_historial.html',datos)
        else:
            datos={"r2":'No tiene permisos para acceder a esta Pagina!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
            return render(request,'index.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#--------------------------------------------------------------------------------------------------
def buscarProfesor(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if request.method=="POST":
            id=request.POST["oppro"]
            p=Profesor.objects.filter(id=id)
            if p:
                comprobarHor=Horario.objects.filter(profesor_id=id)
                if comprobarHor:
                    hor=Horario.objects.select_related("profesor").filter(profesor_id=id).order_by("curso_id")
                    lun1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=1).order_by("curso_id")
                    lun2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=2).order_by("curso_id")
                    lun3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=3).order_by("curso_id")
                    lun4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=4).order_by("curso_id")
                    lun5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=5).order_by("curso_id")
                    lun6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=6).order_by("curso_id")
                    lun7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=7).order_by("curso_id")
                    lun8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=8).order_by("curso_id")
                    lun9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=9).order_by("curso_id")
                    mar1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=1).order_by("curso_id")
                    mar2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=2).order_by("curso_id")
                    mar3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=3).order_by("curso_id")
                    mar4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=4).order_by("curso_id")
                    mar5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=5).order_by("curso_id")
                    mar6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=6).order_by("curso_id")
                    mar7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=7).order_by("curso_id")
                    mar8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=8).order_by("curso_id")
                    mar9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=9).order_by("curso_id")
                    mie1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=1).order_by("curso_id")
                    mie2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=2).order_by("curso_id")
                    mie3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=3).order_by("curso_id")
                    mie4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=4).order_by("curso_id")
                    mie5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=5).order_by("curso_id")
                    mie6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=6).order_by("curso_id")
                    mie7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=7).order_by("curso_id")
                    mie8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=8).order_by("curso_id")
                    mie9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=9).order_by("curso_id")
                    jue1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=1).order_by("curso_id")
                    jue2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=2).order_by("curso_id")
                    jue3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=3).order_by("curso_id")
                    jue4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=4).order_by("curso_id")
                    jue5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=5).order_by("curso_id")
                    jue6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=6).order_by("curso_id")
                    jue7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=7).order_by("curso_id")
                    jue8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=8).order_by("curso_id")
                    jue9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=9).order_by("curso_id")
                    vie1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=1).order_by("curso_id")
                    vie2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=2).order_by("curso_id")
                    vie3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=3).order_by("curso_id")
                    vie4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=4).order_by("curso_id")
                    vie5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=5).order_by("curso_id")
                    vie6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=6).order_by("curso_id")
                    vie7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=7).order_by("curso_id")
                    vie8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=8).order_by("curso_id")
                    vie9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=9).order_by("curso_id")
                    pro=Profesor.objects.all().order_by("id")
                    rs=Profesor.objects.filter(id=id)
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"hor":hor,"r":'El Profesor posee horario registrado!!',"rs":rs,"lun1":lun1,"lun2":lun2,"lun3":lun3,"lun4":lun4,"lun5":lun5,"lun6":lun6,"lun7":lun7,"lun8":lun8,"lun9":lun9,"mar1":mar1,"mar2":mar2,"mar3":mar3,"mar4":mar4,"mar5":mar5,"mar6":mar6,"mar7":mar7,"mar8":mar8,"mar9":mar9,"mar1":mie1,"mie2":mie2,"mie3":mie3,"mie4":mie4,"mie5":mie5,"mie6":mie6,"mie7":mie7,"mie8":mie8,"mie9":mie9,"jue1":jue1,"jue2":jue2,"jue3":jue3,"jue4":jue4,"jue5":jue5,"jue6":jue6,"jue7":jue7,"jue8":jue8,"jue9":jue9,"vie1":vie1,"vie2":vie2,"vie3":vie3,"vie4":vie4,"vie5":vie5,"vie6":vie6,"vie7":vie7,"vie8":vie8,"vie9":vie9}
                    return render(request,'visualizar_horarios_profesor.html',datos)
                else:
                    pro=Profesor.objects.all().order_by("id")
                    datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"r3":'El Profesor no posee Horario Registrado!!'}
                    return render(request,'visualizar_horarios_profesor.html',datos)
            else:
                pro=Profesor.objects.all().order_by("id")
                datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"r2":'Profesor no Registrado!!'}
                return render(request,'visualizar_horarios_profesor.html',datos)
        else:
            pro=Profesor.objects.all().order_by("id")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro,"r2":'Debe Presionar el Boton de Busqueda!!'}
            return render(request,'visualizar_horarios_profesor.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)
#-------------------------------------------------------------------------
@role_required(['DIRECTOR', 'PROFESOR', 'ADMINISTRADOR'])
@profesor_data_only
def mostrarHorarioProfesor(request):
    nomUsuario=request.session.get("nomUsuario")
    cargoUsuario=request.session.get("cargoUsuario")
    if nomUsuario:
        if cargoUsuario == "PROFESOR":
            idUsuario=request.session.get("idUsuario")
            datpro=Profesor.objects.filter(usuario_id=idUsuario)
            idp=Profesor.objects.get(usuario_id=idUsuario)
            id=idp.id
            comprobarHor=Horario.objects.filter(profesor_id=id)
            if comprobarHor:
                hor=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id).order_by("curso_id")
                lun1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=1).order_by("curso_id")
                lun2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=2).order_by("curso_id")
                lun3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=3).order_by("curso_id")
                lun4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=4).order_by("curso_id")
                lun5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=5).order_by("curso_id")
                lun6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=6).order_by("curso_id")
                lun7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=7).order_by("curso_id")
                lun8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=8).order_by("curso_id")
                lun9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="LUNES",bloque=9).order_by("curso_id")
                mar1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=1).order_by("curso_id")
                mar2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=2).order_by("curso_id")
                mar3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=3).order_by("curso_id")
                mar4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=4).order_by("curso_id")
                mar5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=5).order_by("curso_id")
                mar6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=6).order_by("curso_id")
                mar7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=7).order_by("curso_id")
                mar8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=8).order_by("curso_id")
                mar9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MARTES",bloque=9).order_by("curso_id")
                mie1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=1).order_by("curso_id")
                mie2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=2).order_by("curso_id")
                mie3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=3).order_by("curso_id")
                mie4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=4).order_by("curso_id")
                mie5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=5).order_by("curso_id")
                mie6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=6).order_by("curso_id")
                mie7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=7).order_by("curso_id")
                mie8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=8).order_by("curso_id")
                mie9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="MIERCOLES",bloque=9).order_by("curso_id")
                jue1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=1).order_by("curso_id")
                jue2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=2).order_by("curso_id")
                jue3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=3).order_by("curso_id")
                jue4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=4).order_by("curso_id")
                jue5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=5).order_by("curso_id")
                jue6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=6).order_by("curso_id")
                jue7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=7).order_by("curso_id")
                jue8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=8).order_by("curso_id")
                jue9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="JUEVES",bloque=9).order_by("curso_id")
                vie1=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=1).order_by("curso_id")
                vie2=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=2).order_by("curso_id")
                vie3=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=3).order_by("curso_id")
                vie4=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=4).order_by("curso_id")
                vie5=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=5).order_by("curso_id")
                vie6=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=6).order_by("curso_id")
                vie7=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=7).order_by("curso_id")
                vie8=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=8).order_by("curso_id")
                vie9=Horario.objects.select_related("asignatura","curso").filter(profesor_id=id,dia="VIERNES",bloque=9).order_by("curso_id")

                datos={
                    "datpro":datpro,
                    "cargo":cargoUsuario,
                    "hor":hor,
                    "lun1":lun1,"lun2":lun2,"lun3":lun3,"lun4":lun4,"lun5":lun5,"lun6":lun6,"lun7":lun7,"lun8":lun8,"lun9":lun9,
                    "mar1":mar1,"mar2":mar2,"mar3":mar3,"mar4":mar4,"mar5":mar5,"mar6":mar6,"mar7":mar7,"mar8":mar8,"mar9":mar9,
                    "mie1":mie1,"mie2":mie2,"mie3":mie3,"mie4":mie4,"mie5":mie5,"mie6":mie6,"mie7":mie7,"mie8":mie8,"mie9":mie9,
                    "jue1":jue1,"jue2":jue2,"jue3":jue3,"jue4":jue4,"jue5":jue5,"jue6":jue6,"jue7":jue7,"jue8":jue8,"jue9":jue9,
                    "vie1":vie1,"vie2":vie2,"vie3":vie3,"vie4":vie4,"vie5":vie5,"vie6":vie6,"vie7":vie7,"vie8":vie8,"vie9":vie9
                }
                return render(request, 'visualizar_horarios_profesor.html', datos)
            else:
                datos={"datpro":datpro,"cargo":cargoUsuario}
                return render(request, 'visualizar_horarios_profesor.html', datos)
        else:
            pro=Profesor.objects.all().order_by("id")
            datos={"nomUsuario":nomUsuario,"cargo":cargoUsuario,"pro":pro}
            return render(request,'visualizar_horarios_profesor.html',datos)
    else:
        datos={"r2":'Debe Iniciar Sesion!!',"uc":'Cursos y Usuarios cargados correctamente!!'}
        return render(request,'index.html',datos)

#---------------------------------------------------------------------------------
def forgot_password(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.core.mail import send_mail
    from django.conf import settings
    from .models import Profesor, OTPCode
    from django.contrib.auth.models import User
    import random
    import string
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Verificar si existe al menos un usuario con ese email
        if User.objects.filter(email=email).exists():
            
            # Generar código OTP de 6 dígitos
            otp_code = ''.join(random.choices(string.digits, k=6))
            
            # Eliminar códigos OTP anteriores para este email
            OTPCode.objects.filter(email=email).delete()
            
            # Crear nuevo código OTP
            OTPCode.objects.create(email=email, code=otp_code)
            
            # Enviar email con el código OTP
            try:
                send_mail(
                    'Código de Recuperación de Contraseña - Sistema Educacional',
                    f'Su código de verificación es: {otp_code}\n\nEste código expira en 5 minutos.\n\nSi no solicitó este código, ignore este mensaje.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                # Guardar email en sesión para verificación posterior
                request.session['reset_email'] = email
                messages.success(request, 'Código OTP enviado a su correo electrónico')
                return redirect('otp')
                
            except Exception as e:
                print(f"Error al enviar correo: {str(e)}")
                messages.error(request, f'Error al enviar el correo: {str(e)}. Verifique la configuración de correo.')
        else:
            messages.error(request, 'No existe un usuario registrado con ese correo electrónico')
    
    return render(request, 'forgot_password.html')

#---------------------------------------------------------------------------------
def verify_otp(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    from .models import OTPCode
    
    # Verificar que hay un email en sesión
    reset_email = request.session.get('reset_email')
    if not reset_email:
        messages.error(request, 'Sesión expirada. Solicite un nuevo código.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        
        try:
            # Buscar el código OTP más reciente para este email
            otp_record = OTPCode.objects.filter(
                email=reset_email, 
                code=otp_code, 
                is_used=False
            ).first()
            
            if otp_record:
                if not otp_record.is_expired():
                    # Marcar el código como usado
                    otp_record.is_used = True
                    otp_record.save()
                    
                    # Guardar verificación en sesión
                    request.session['otp_verified'] = True
                    messages.success(request, 'Código OTP verificado correctamente')
                    return redirect('reset_password')
                else:
                    messages.error(request, 'El código OTP ha expirado. Solicite uno nuevo.')
            else:
                messages.error(request, 'Código OTP inválido')
                
        except Exception as e:
            messages.error(request, 'Error al verificar el código')
    
    return render(request, 'verify_otp.html')

#---------------------------------------------------------------------------------
def resend_otp(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.core.mail import send_mail
    from django.conf import settings
    from .models import OTPCode
    import random
    import string
    
    reset_email = request.session.get('reset_email')
    if not reset_email:
        messages.error(request, 'Sesión expirada. Solicite un nuevo código.')
        return redirect('forgot_password')
    
    try:
        # Generar nuevo código OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Eliminar códigos anteriores
        OTPCode.objects.filter(email=reset_email).delete()
        
        # Crear nuevo código
        OTPCode.objects.create(email=reset_email, code=otp_code)
        
        # Enviar email
        send_mail(
            'Código de Recuperación de Contraseña - Sistema Educacional',
            f'Su nuevo código de verificación es: {otp_code}\n\nEste código expira en 5 minutos.',
            settings.DEFAULT_FROM_EMAIL,
            [reset_email],
            fail_silently=False,
        )
        
        messages.success(request, 'Nuevo código OTP enviado a su correo electrónico')
    except Exception as e:
        messages.error(request, 'Error al reenviar el código')
    
    return redirect('otp')

#---------------------------------------------------------------------------------
def reset_password(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.contrib.auth.models import User
    from .models import Profesor
    
    # Verificar que el OTP fue verificado
    if not request.session.get('otp_verified'):
        messages.error(request, 'Debe verificar el código OTP primero')
        return redirect('otp')
    
    reset_email = request.session.get('reset_email')
    if not reset_email:
        messages.error(request, 'Sesión expirada')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
        elif len(new_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
        else:
            try:
                # Buscar usuarios por email (puede haber más de uno)
                users = User.objects.filter(email=reset_email)
                
                if not users.exists():
                    raise User.DoesNotExist
                
                for user in users:
                    # Cambiar la contraseña en User
                    user.set_password(new_password)
                    user.save()
                    
                    # También cambiar en Usuario si existe (usando la relación ForeignKey)
                    usuarios = Usuario.objects.filter(user=user)
                    for usuario in usuarios:
                        usuario.password = new_password
                        usuario.save()
                
                # Limpiar sesión
                request.session.pop('reset_email', None)
                request.session.pop('otp_verified', None)
                
                messages.success(request, 'Contraseña cambiada exitosamente. Puede iniciar sesión con su nueva contraseña.')
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, 'Error al cambiar la contraseña: Usuario no encontrado')
            except Exception as e:
                print(f"Error al cambiar contraseña: {str(e)}")
                messages.error(request, f'Error al cambiar la contraseña: {str(e)}')
    
    return render(request, 'reset_password.html')

def registrar_alumno(request):
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

# ===== FUNCIONES DE EXPORTACIÓN =====

def exportar_alumnos_excel(request):
    """Exportar lista de alumnos a Excel"""
    from django.http import HttpResponse
    import openpyxl
    from django.contrib.auth.models import User
    from django.db.models.fields.files import ImageFieldFile
    from .models import Alumnos
    
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

@role_required(["ADMINISTRADOR"])
def generar_certificados_pdf(request):
    import io
    import os
    from django.http import FileResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from zipfile import ZipFile
    from .models import Certificados
    try:
        from PyPDF2 import PdfReader, PdfWriter
    except Exception:
        PdfReader = None
        PdfWriter = None
    certificados_ids = request.GET.getlist('certificados')
    if certificados_ids:
        certificados = Certificados.objects.filter(idCertificado__in=certificados_ids)
    else:
        certificados = Certificados.objects.all()
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        for certificado in certificados:
            alumno = certificado.idMatricula
            use_template = certificado.TipoCertificado == "CERTIFICADO DE ALUMNO REGULAR" and PdfReader is not None and PdfWriter is not None
            template_candidates = [
                os.path.join("staticfiles", "certificados", "certificado_13256254.pdf"),
                os.path.join("staticfiles", "certificado_13256254.pdf"),
                "certificado_13256254.pdf",
            ]
            template_path = next((p for p in template_candidates if os.path.exists(p)), None)
            if use_template and template_path:
                reader = PdfReader(template_path)
                page = reader.pages[0]
                width = float(page.mediabox.right) - float(page.mediabox.left)
                height = float(page.mediabox.top) - float(page.mediabox.bottom)
                overlay_buffer = io.BytesIO()
                c = canvas.Canvas(overlay_buffer, pagesize=(width, height))
                c.setFont("Helvetica-Bold", 16)
                inst = "Instituto Lautaro de Codegua"
                inst_w = c.stringWidth(inst, "Helvetica-Bold", 16)
                c.drawString((width - inst_w) / 2, height - 60, inst)
                c.setFont("Helvetica", 12)
                c.drawString(100, height - 120, "Certificado de Alumno Regular")
                c.drawString(100, height - 150, f"Nombre: {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
                c.drawString(100, height - 170, f"RUN: {alumno.run}")
                c.drawString(100, height - 190, f"Curso: {alumno.curso}")
                c.save()
                overlay_buffer.seek(0)
                overlay_reader = PdfReader(overlay_buffer)
                writer = PdfWriter()
                base_page = reader.pages[0]
                base_page.merge_page(overlay_reader.pages[0])
                writer.add_page(base_page)
                output_buffer = io.BytesIO()
                writer.write(output_buffer)
                output_buffer.seek(0)
                pdf_filename = f"certificado_{certificado.idCertificado}.pdf"
                zip_file.writestr(pdf_filename, output_buffer.getvalue())
            else:
                buffer = io.BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)
                width, height = letter
                inst = "Instituto Lautaro de Codegua"
                p.setFont("Helvetica-Bold", 16)
                inst_w = p.stringWidth(inst, "Helvetica-Bold", 16)
                p.drawString((width - inst_w) / 2, height - 60, inst)
                p.setFont("Helvetica", 12)
                p.drawString(100, height - 120, f"Certificado de {certificado.TipoCertificado}")
                p.drawString(100, height - 150, f"Nombre: {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
                p.drawString(100, height - 170, f"RUN: {alumno.run}")
                p.drawString(100, height - 190, f"Curso: {alumno.curso}")
                p.save()
                buffer.seek(0)
                pdf_filename = f"certificado_{certificado.idCertificado}.pdf"
                zip_file.writestr(pdf_filename, buffer.getvalue())
    zip_buffer.seek(0)
    if certificados_ids:
        Certificados.objects.filter(idCertificado__in=certificados_ids).update(EstadoCertificado='SIN ENTREGAR')
    return FileResponse(zip_buffer, as_attachment=True, filename="certificados.zip")

def listar_alumnos(request):
    """Vista para listar alumnos con opción de exportar"""
    from .models import Alumnos
    
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

@role_required(["ADMINISTRADOR", "DIRECTOR"])
def listar_certificados(request):
    """Vista para listar certificados con opción de generar PDF"""
    from .models import Certificados
    
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if nomUsuario:
        certificados = Certificados.objects.all().order_by('-FechaHoraRegistroCertificado')
        
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'cargo': cargoUsuario,
            'certificados': certificados,
            'titulo': 'Lista de Certificados'
        }
        
        return render(request, 'listar_certificados.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

def mostrar_registrar_certificado(request):
    """Mostrar formulario para registrar certificado"""
    from .models import Alumnos
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    if nomUsuario:
        alumnos = Alumnos.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombre')
        context = {
            'nomUsuario': nomUsuario,
            'cargoUsuario': cargoUsuario,
            'cargo': cargoUsuario,
            'alumnos': alumnos,
            'titulo': 'Registrar Certificado'
        }
        return render(request, 'registrar_certificado.html', context)
    else:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)

def registrar_certificado(request):
    """Procesar registro de certificado"""
    from django.contrib import messages
    from .models import Certificados, Alumnos, Usuario
    if request.method == "POST":
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario:
            try:
                alumno_id = request.POST.get('alumno_id')
                tipo = request.POST.get('tipo')
                motivo = "EL que estime conveniente"
                lugar = "EL que estime conveniente"
                estado = request.POST.get('estado') or 'PENDIENTE'

                alumno = Alumnos.objects.get(matricula=alumno_id)

                usuario_id = request.session.get("idUsuario")
                usuario = Usuario.objects.get(id=usuario_id)

                certificado = Certificados(
                    idMatricula=alumno,
                    TipoCertificado=tipo,
                    MotivoCertificado=motivo,
                    LugarPresentacionCertificado=lugar,
                    Administrativo=usuario.user,
                    EstadoCertificado=estado,
                )
                certificado.save()

                messages.success(request, 'Certificado registrado correctamente!')
                return redirect('listar_certificados')
            except Alumnos.DoesNotExist:
                messages.error(request, 'Alumno no encontrado')
                return redirect('mostrar_registrar_certificado')
            except Exception as e:
                messages.error(request, f'Error al registrar el certificado: {str(e)}')
                return redirect('mostrar_registrar_certificado')
        else:
            datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
            return render(request, 'index.html', datos)
    else:
        return redirect('mostrar_registrar_certificado')

@role_required(['DIRECTOR', 'PROFESOR', 'ESTUDIANTE', 'ALUMNO', 'ADMINISTRADOR'])
def mostrar_perfil(request):
    """Vista para mostrar el perfil del usuario según su tipo (PROFESOR o ESTUDIANTE)"""
    nomUsuario = request.session.get("nomUsuario")
    cargoUsuario = request.session.get("cargoUsuario")
    
    if not nomUsuario:
        datos = {"r2": 'Debe Iniciar Sesion!!', "uc": 'Cursos y Usuarios cargados correctamente!!'}
        return render(request, 'index.html', datos)
    
    context = {
        'nomUsuario': nomUsuario,
        'cargoUsuario': cargoUsuario,
        'cargo': cargoUsuario,
    }
    
    
    if cargoUsuario == "PROFESOR":
        idAuthUser = request.session.get("idAuthUser")
        profesor_qs = Profesor.objects.filter(usuario_id=idAuthUser)
        if not profesor_qs.exists():
            profesor_qs = Profesor.objects.filter(email=nomUsuario.lower())
        profesor = profesor_qs.first()
        if profesor:
            especialidades = AsignaturasProfesor.objects.filter(profesor_id=profesor.id)
            datpro = Profesor.objects.filter(id=profesor.id).values()
            context.update({
                'es_profesor': True,
                'profesor': profesor,
                'especialidades': especialidades,
                'datpro': datpro,
                'cargo': cargoUsuario
            })
        else:
            context.update({'es_profesor': False, 'cargo': cargoUsuario})
        
    elif cargoUsuario == "ESTUDIANTE" or cargoUsuario == "ALUMNO":
        idAuthUser = request.session.get("idAuthUser") or (request.user.id if getattr(request, "user", None) and request.user.is_authenticated else None)
        idUsuario = request.session.get("idUsuario")
        candidato_user_ids = []
        if idAuthUser:
            candidato_user_ids.append(idAuthUser)
        if idUsuario:
            u = Usuario.objects.filter(id=idUsuario).first()
            if u and u.user_id:
                candidato_user_ids.append(u.user_id)
        if getattr(request, "user", None) and request.user.is_authenticated:
            candidato_user_ids.append(request.user.id)
        candidato_user_ids = list(dict.fromkeys(candidato_user_ids))

        alumno = None
        for uid in candidato_user_ids:
            if not alumno:
                alumno = Alumnos.objects.filter(user_id=uid).first()
        if not alumno and getattr(request.user, "email", None):
            alumno = Alumnos.objects.filter(email__iexact=request.user.email).first()
        if not alumno and nomUsuario:
            alumno = Alumnos.objects.filter(email__iexact=nomUsuario).first()
        if not alumno and nomUsuario:
            alumno = Alumnos.objects.filter(run__iexact=nomUsuario).first()

        padre = None
        apoderado = None

        if alumno:
            try:
                padre = Padre.objects.get(alumno=alumno)
            except Padre.DoesNotExist:
                padre = None
            try:
                apoderado = Apoderado.objects.get(alumno=alumno)
            except Apoderado.DoesNotExist:
                apoderado = None
            datest = Alumnos.objects.filter(matricula=alumno.matricula).values()
            context.update({'datest': datest, 'cargo': cargoUsuario})
            context.update({
                'es_estudiante': True,
                'alumno': alumno,
                'padre': padre,
                'apoderado': apoderado
            })
        else:
            datest = Alumnos.objects.filter(email__iexact=nomUsuario).values()
            if not datest and getattr(request.user, "email", None):
                datest = Alumnos.objects.filter(email__iexact=request.user.email).values()
            context.update({'datest': datest, 'cargo': cargoUsuario})
            context.update({'es_estudiante': False})
            
    
    return render(request, 'perfil.html', context)

@login_required
def cambiar_password(request):
    """Vista para procesar el cambio de contraseña"""
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmacion = request.POST.get('password_confirmacion')
        
        user = request.user
        
        if not user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('perfil')
            
        if password_nueva != password_confirmacion:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
            return redirect('perfil')
            
        user.set_password(password_nueva)
        user.save()

        # Actualizar contraseña en tabla horarios_usuario
        try:
            # Buscar el usuario en la tabla personalizada usando el nombre de usuario (que es único en el sistema)
            # La tabla Usuario guarda la contraseña en texto plano, mientras que auth_user la guarda hasheada
            nombre_usuario = user.username
            
            # Intentar buscar por el campo user (Foreign Key)
            usuarios = Usuario.objects.filter(user=user)
            
            # Si no se encuentra por FK, intentar por nombre (fallback)
            if not usuarios.exists():
                usuarios = Usuario.objects.filter(nombre=nombre_usuario)
            
            if usuarios.exists():
                for usuario in usuarios:
                    # Guardamos la contraseña en texto plano porque así lo maneja el login personalizado
                    usuario.password = password_nueva
                    usuario.save()
            else:
                print(f"Advertencia: No se encontró registro en tabla Usuario para {nombre_usuario}")
                
        except Exception as e:
            print(f"Error actualizando tabla Usuario: {e}")

        update_session_auth_hash(request, user)  # Mantener la sesión activa
        messages.success(request, 'Contraseña actualizada correctamente.')
        return redirect('perfil')
    
    return redirect('perfil')


#-------------------------------------------------------------------------------------------------
#---------------------------------------Gestión de Actividades-----------------------------------
#-------------------------------------------------------------------------------------------------

@role_required(['DIRECTOR', 'PROFESOR', 'ESTUDIANTE', 'ADMINISTRADOR'])
def listar_actividades(request):
    """Vista para listar todas las actividades"""
    from .models import Actividades
    
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

def mostrar_registrar_actividad(request):
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

def registrar_actividad(request):
    """Vista para procesar el registro de una nueva actividad"""
    from .models import Actividades, Usuario
    
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

def mostrar_modificar_actividad(request, hash_id):
    """Vista para mostrar el formulario de modificación de actividad"""
    from .models import Actividades
    
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

# ==================== GESTIÓN DE PADRES/APODERADOS ====================

def listar_padres(request):
    """Vista para listar todos los padres/apoderados"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    from .models import Padre, Alumnos
    
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

def mostrar_registrar_padre(request):
    """Vista para mostrar el formulario de registro de padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    from .models import Alumnos
    
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

def registrar_padre(request):
    """Vista para procesar el registro de un nuevo padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        from .models import Padre, Alumnos
        
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

def mostrar_modificar_padre(request, id_padre):
    """Vista para mostrar el formulario de modificación de padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    from .models import Padre, Alumnos
    
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

def modificar_padre(request, id_padre):
    """Vista para procesar la modificación de un padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        from .models import Padre, Alumnos
        
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

def eliminar_padre(request, id_padre):
    """Vista para eliminar un padre"""
    if 'nomUsuario' not in request.session:
        return redirect('login')
    
    try:
        from .models import Padre
        
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

#-------------------------------------------------------------------------------------------------
#---------------------------------Vistas para Impresiones-------------------------------------
#-------------------------------------------------------------------------------------------------

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

# Fin de las vistas para Impresiones
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#---------------------------------------Gestión de Atenciones------------------------------------
#-------------------------------------------------------------------------------------------------

@role_required(["ADMINISTRADOR", "PROFESOR"])
def listar_atenciones(request):
    """Vista para listar todas las atenciones"""
    from .models import Atenciones
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
def mostrar_registrar_atencion(request):
    """Vista para mostrar el formulario de registro de atenciones"""
    from .models import Alumnos
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
def registrar_atencion(request):
    """Vista para procesar el registro de una nueva atención"""
    from .models import Atenciones, Alumnos
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
def mostrar_modificar_atencion(request, hash_id):
    """Vista para mostrar el formulario de modificación de atención"""
    from .models import Atenciones, Alumnos
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

#-------------------------------------------------------------------------------------------------
#---------------------------------------Gestión de Insumos---------------------------------------
#-------------------------------------------------------------------------------------------------

@role_required(["ADMINISTRADOR","DIRECTOR"])
def listar_insumos(request):
    """Vista para listar todos los insumos"""
    from .models import Insumos
    
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
    from .models import Insumos
    
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
    from .models import Insumos
    
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
    from .models import Insumos
    
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
    from .models import Insumos
    
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

# ==================== GESTIÓN DE PRÉSTAMOS ====================

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

#=================================================================================================
#================================ GESTIÓN DE CONSEJOS DE PROFESORES ========================
#=================================================================================================

@role_required(["ADMINISTRADOR", "DIRECTOR"])
def listar_consejos(request):
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
def mostrar_registrar_consejo(request):
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
def registrar_consejo(request):
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
def mostrar_modificar_consejo(request, id_consejo):
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
def modificar_consejo(request, id_consejo):
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
def eliminar_consejo(request, id_consejo):
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

@role_required(["ADMINISTRADOR", "PROFESOR"])
def modificar_atencion(request, hash_id):
    """Vista para procesar la modificación de una atención"""
    from .models import Atenciones, Alumnos
    
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
def eliminar_atencion(request, hash_id):
    """Vista para eliminar una atención"""
    from .models import Atenciones
    
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

def modificar_actividad(request, hash_id):
    """Vista para procesar la modificación de una actividad"""
    from .models import Actividades
    
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

def eliminar_actividad(request, hash_id):
    """Vista para eliminar una actividad"""
    from .models import Actividades
    
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
