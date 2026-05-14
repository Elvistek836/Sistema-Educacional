from datetime import datetime
from django.shortcuts import render
from horarios.models import Profesor, DisponibilidadProfesor, Horario, Historial
from django.http import HttpRequest
from horarios.decorators import role_required, profesor_data_only

@role_required(['DIRECTOR', 'PROFESOR', 'ADMINISTRADOR'])
@profesor_data_only
def mostrarVisualizarDisp(request: HttpRequest):
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
def mostrarRegistrarDis(request: HttpRequest, hash_id: str):
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
def buscarProfesorDis(request: HttpRequest, hash_id: str):
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
def cambiarDisponibilidad(request: HttpRequest, id: int, id2: int):
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
