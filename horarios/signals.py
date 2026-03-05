from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profesor, DisponibilidadProfesor, Alumnos, Usuario

@receiver(post_save, sender=Profesor)
def crear_usuario(sender, instance, created, **kwargs):
    if created:
        # El usuario se crea en la vista registrarProfesor, no aqui.
        # Evitamos duplicidad y errores de integridad.
        
        id=instance.id
        estado="NO DISPONIBLE"
        dia1="LUNES"
        dia2="MARTES"
        dia3="MIERCOLES"
        dia4="JUEVES"
        dia5="VIERNES"
        d=DisponibilidadProfesor(bloque=1,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=2,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=3,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=4,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=5,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=6,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=7,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=8,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=9,dia=dia1,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=1,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=2,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=3,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=4,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=5,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=6,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=7,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=8,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=9,dia=dia2,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=1,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=2,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=3,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=4,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=5,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=6,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=7,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=8,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=9,dia=dia3,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=1,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=2,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=3,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=4,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=5,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=6,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=7,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=8,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=9,dia=dia4,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=1,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=2,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=3,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=4,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=5,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=6,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=7,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=8,dia=dia5,estado=estado,profesor_id=id)
        d.save()
        d=DisponibilidadProfesor(bloque=9,dia=dia5,estado=estado,profesor_id=id)
        d.save()

@receiver(post_save, sender=Alumnos)
def crear_usuario_alumno(sender, instance, created, **kwargs):
    if created and instance.email:
        user = User.objects.filter(email=instance.email).first()
        if not user:
            username = instance.run or instance.matricula or instance.email
            user = User.objects.create_user(
                username=username,
                email=instance.email,
                password="Ingresar01"
            )
            user.first_name = instance.nombre or ""
            user.last_name = instance.apellido_paterno or ""
            user.is_staff = True
            user.save()

        if not instance.user:
            instance.user = user
            instance.save(update_fields=["user"]) 

        try:
            if not Usuario.objects.filter(user=user).exists():
                Usuario.objects.create(nombre=user.username, password="Ingresar01", cargo="ESTUDIANTE", user=user)
        except Exception:
            pass