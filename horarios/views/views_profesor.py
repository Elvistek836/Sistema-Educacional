from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from horarios.models import Profesor, Asignatura, Curso, AsignaturasProfesor, DisponibilidadProfesor, Horario, Usuario, Historial, Alumnos, Padre, Apoderado, Impresiones, Insumos, Prestamos, ConsejosProfesores, CURSOS_CHOICE, ESTADOIMPRESION_CHOICES
from horarios.decorators import role_required, profesor_data_only, alumno_data_only, login_or_session_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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