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