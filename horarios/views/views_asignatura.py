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