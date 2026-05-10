from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from horarios.models import Profesor, Curso, AsignaturasProfesor,Horario, Usuario, Historial, Alumnos, Padre, Apoderado
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from horarios.decorators import role_required

@login_required
def cambiar_password(request: HttpRequest):
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

@role_required(['DIRECTOR', 'PROFESOR', 'ESTUDIANTE', 'ALUMNO', 'ADMINISTRADOR'])
def mostrar_perfil(request: HttpRequest):
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

def reset_password(request: HttpRequest):
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

def resend_otp(request: HttpRequest):
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

def verify_otp(request: HttpRequest):
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

def forgot_password(request: HttpRequest):
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

def cerrarSesion(request: HttpRequest):
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

def iniciarSesion(request: HttpRequest):
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

def registrar(request: HttpRequest):
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

def registrarCursos(request: HttpRequest):
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

def registrarUsuarios(request: HttpRequest):

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

def mostrarIndex(request: HttpRequest):
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

def mostrarMenu(request: HttpRequest):
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

def mostrarHistorial(request: HttpRequest):
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