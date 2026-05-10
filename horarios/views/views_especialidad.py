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
