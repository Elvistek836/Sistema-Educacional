from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
import uuid
from horarios.models import (
    Profesor, Curso, Asignatura, AsignaturasProfesor, DisponibilidadProfesor,
    Horario, Alumnos, Apoderado, Padre, Actividades, Prestamos, Insumos,
    Impresiones, ConsejosProfesores, Certificados, Atenciones, Usuario
)

class Command(BaseCommand):
    help = "Simula registros en todas las formas y luego los borra"

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep",
            action="store_true",
            help="Mantiene los registros de prueba creados (no los elimina)",
        )

    def handle(self, *args, **options):
        suffix = timezone.now().strftime("%Y%m%d%H%M%S")
        rand = uuid.uuid4().hex[:8]
        def next_id(model, field_name="id"):
            max_val = model.objects.aggregate(Max(field_name)).get(f"{field_name}__max")
            return (max_val or 0) + 1
        created = {
            "users": [],
            "profesores": [],
            "cursos": [],
            "asignaturas": [],
            "asignaturas_profesor": [],
            "disponibilidades": [],
            "horarios": [],
            "alumnos": [],
            "padres": [],
            "apoderados": [],
            "actividades": [],
            "atenciones": [],
            "insumos": [],
            "prestamos": [],
            "certificados": [],
            "consejos": [],
            "impresiones": [],
        }

        try:
            # Usuarios fijos para pruebas de UI
            admin_user, _ = User.objects.get_or_create(username="admin_test_ui", defaults={"email": "admin_ui@example.com"})
            admin_user.set_password("admin12345")
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            created["users"].append(admin_user)

            prof_user, _ = User.objects.get_or_create(username="prof_test_ui", defaults={"email": "prof_ui@example.com"})
            prof_user.set_password("prof12345")
            prof_user.is_staff = True
            prof_user.save()
            created["users"].append(prof_user)

            profesor, _ = Profesor.objects.get_or_create(
                id=next_id(Profesor, "id"),
                defaults={
                    "usuario": prof_user,
                    "rut": f"{suffix[:2]}.{suffix[2:5]}.{suffix[5:8]}-{suffix[-1]}",
                    "nombre": "Profesor Test",
                    "apellido": "Ejemplo",
                    "nivel": "BASICA y MEDIA",
                    "email": "prof_ui@example.com",
                }
            )
            created["profesores"].append(profesor)

            curso = Curso.objects.create(nombre=f"CURSO PRUEBA {suffix}-{rand}")
            created["cursos"].append(curso)

            asignatura = Asignatura.objects.create(
                id=next_id(Asignatura, "id"),
                codigo=f"ASG-{suffix}-{rand}",
                nombre="Lenguaje y Comunicación (1ero a 4to Basico) - 8hrs",
                nivel="BASICA",
                bloques=8,
                curso=curso,
            )
            created["asignaturas"].append(asignatura)

            asp = AsignaturasProfesor.objects.create(
                id=next_id(AsignaturasProfesor, "id"),
                nombre="Lengua y Literatura (7mo a 2do Medio) - 6hrs",
                nivel="BASICA y MEDIA",
                profesor=profesor,
            )
            created["asignaturas_profesor"].append(asp)

            disp = DisponibilidadProfesor.objects.create(
                id=next_id(DisponibilidadProfesor, "id"),
                bloque=1,
                dia="LUNES",
                estado="DISPONIBLE",
                profesor_id=profesor.id,
            )
            created["disponibilidades"].append(disp)

            horario = Horario.objects.create(
                id=next_id(Horario, "id"),
                bloque=1,
                dia="LUNES",
                asignatura=asignatura,
                curso=curso,
                profesor=profesor,
            )
            created["horarios"].append(horario)

            alumno = Alumnos.objects.create(
                matricula=next_id(Alumnos, "matricula"),
                Administrativo=admin_user,
                curso="PRIMERO BASICO",
                run=f"{suffix[:2]}{suffix[2:5]}{suffix[5:8]}-{suffix[-1]}",
                nombre="Alumno",
                apellido_paterno="Prueba",
                apellido_materno="Ejemplo",
                direccion="Calle Falsa 123",
                comuna="Rancagua",
                procedencia="Prueba",
                curso_repetido="NO APLICA",
                con_quien_vive="Familia",
                enfermedad="Ninguna",
                prevision="Ninguna",
                letra_fonasa="NO APLICA",
                alimentacion_establecimiento="No",
                programa_solidario="No",
                programa="Ninguno",
                locomocion="Bus",
                fono_locomocion="912345678",
                vive_con="Padres",
                emergencia="123456789",
                complementarios="",
            )
            created["alumnos"].append(alumno)

            padre = Padre.objects.create(
                id=next_id(Padre, "id"),
                alumno=alumno,
                es_madre=False,
                run=f"{suffix[:2]}{suffix[2:5]}{suffix[5:8]}-{suffix[-1]}",
                nombre="Padre",
                apellido_paterno="Prueba",
                apellido_materno="Ejemplo",
                fono="912345678",
                escolaridad="MEDIA COMPLETA",
                ocupacion="Empleado",
                edad=40,
                religion="No aplica",
            )
            created["padres"].append(padre)

            apoderado = Apoderado.objects.create(
                id=next_id(Apoderado, "id"),
                alumno=alumno,
                run=f"{suffix[:2]}{suffix[2:5]}{suffix[5:8]}-{suffix[-1]}",
                nombre="Apoderado",
                apellido_paterno="Prueba",
                apellido_materno="Ejemplo",
                fono="912345678",
                escolaridad="MEDIA COMPLETA",
                ocupacion="Empleado",
                edad=38,
                religion="No aplica",
            )
            created["apoderados"].append(apoderado)

            actividad = Actividades.objects.create(
                id=next_id(Actividades, "id"),
                Tipo="ACT. DEPORTIVA",
                Profesor=prof_user,
                Nombre=f"Actividad {suffix}",
                FechaHoraPlanificada=timezone.now() + timedelta(days=7),
                Observacion="Observación de prueba",
                NumeroParticipantesActividad=10,
            )
            created["actividades"].append(actividad)

            atencion = Atenciones.objects.create(
                id=next_id(Atenciones, "id"),
                Tipo="PSICOLOGICA",
                Profesional=admin_user,
                idMatricula=alumno,
                Motivo="CITACION",
                Observaciones="Observaciones de prueba",
            )
            created["atenciones"].append(atencion)

            insumo = Insumos.objects.create(
                NombreInsumo=f"Insumo {suffix}",
                DetalleInsumo="Detalle de prueba",
                StockInsumo=5,
                EstadoInsumo="BUENO",
            )
            created["insumos"].append(insumo)

            prestamo = Prestamos.objects.create(
                Administrativo=admin_user,
                FechaHoraDevolucionPrestamo=timezone.now() + timedelta(days=1),
                DetallePrestamo="Prestamo de prueba",
                EstadoPrestamo="SIN DEVOLVER",
            )
            created["prestamos"].append(prestamo)

            certificado = Certificados.objects.create(
                idMatricula=alumno,
                TipoCertificado="CERTIFICADO DE ALUMNO REGULAR",
                MotivoCertificado="Prueba",
                LugarPresentacionCertificado="Rancagua",
                Administrativo=admin_user,
                EstadoCertificado="PENDIENTE",
            )
            created["certificados"].append(certificado)

            consejo = ConsejosProfesores.objects.create(
                Administrativo=admin_user,
                FechaHoraPlanificadaConsejo=timezone.now() + timedelta(days=14),
                ComentariosConsejo="Comentarios de prueba",
                AcuerdosConsejo="Acuerdos de prueba",
                NumeroProfesoresConsejo=5,
            )
            created["consejos"].append(consejo)

            impresion = Impresiones.objects.create(
                ProfesorImpresion=prof_user,
                FechaHoraUtilizacionImpresion=timezone.now() + timedelta(days=2),
                CursoImpresion="PRIMERO BASICO",
                AsignaturaImpresion="Lenguaje",
                ObservacionImpresion="Observación de prueba",
                EstadoImpresion="PENDIENTE",
            )
            created["impresiones"].append(impresion)

            self.stdout.write(self.style.SUCCESS("Registros de prueba creados"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creando registros: {e}"))

        try:
            if options.get("keep"):
                self.stdout.write(self.style.WARNING("Registros de prueba mantenidos por --keep"))
                return
            for obj in created["impresiones"][::-1]:
                obj.delete()
            for obj in created["consejos"][::-1]:
                obj.delete()
            for obj in created["certificados"][::-1]:
                obj.delete()
            for obj in created["prestamos"][::-1]:
                obj.delete()
            for obj in created["insumos"][::-1]:
                obj.delete()
            for obj in created["atenciones"][::-1]:
                obj.delete()
            for obj in created["actividades"][::-1]:
                obj.delete()
            for obj in created["padres"][::-1]:
                obj.delete()
            for obj in created["apoderados"][::-1]:
                obj.delete()
            for obj in created["alumnos"][::-1]:
                obj.delete()
            for obj in created["horarios"][::-1]:
                obj.delete()
            for obj in created["disponibilidades"][::-1]:
                obj.delete()
            for obj in created["asignaturas_profesor"][::-1]:
                obj.delete()
            for obj in created["asignaturas"][::-1]:
                obj.delete()
            for obj in created["cursos"][::-1]:
                obj.delete()
            for obj in created["profesores"][::-1]:
                obj.delete()
            for obj in created.get("usuarios", [])[::-1]:
                obj.delete()
            for obj in created["users"][::-1]:
                obj.delete()
            self.stdout.write(self.style.SUCCESS("Registros de prueba eliminados"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error eliminando registros: {e}"))
            admin_usu, _ = Usuario.objects.get_or_create(
                id=next_id(Usuario, "id"),
                defaults={
                    "nombre": admin_user.username,
                    "password": "admin12345",
                    "cargo": "ADMINISTRADOR",
                    "user": admin_user,
                }
            )
            prof_usu, _ = Usuario.objects.get_or_create(
                id=next_id(Usuario, "id"),
                defaults={
                    "nombre": prof_user.username,
                    "password": "prof12345",
                    "cargo": "PROFESOR",
                    "user": prof_user,
                }
            )
            created.setdefault("usuarios", []).extend([admin_usu, prof_usu])

            self.stdout.write(self.style.SUCCESS(
                f"Usuarios de prueba: PROFESOR=(prof_test_ui/prof12345), ADMIN=(admin_test_ui/admin12345)"
            ))
            self.stdout.write(self.style.SUCCESS(
                "Puede iniciar sesión en /login con esos usuarios"
            ))