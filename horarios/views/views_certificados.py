from django.shortcuts import render, redirect
from django.http import HttpRequest
from horarios.models import Certificados, Alumnos, Usuario
from horarios.decorators import role_required

@role_required(["ADMINISTRADOR"])
def generar_certificados_pdf(request: HttpRequest):
    import io
    import os
    from django.http import FileResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from zipfile import ZipFile
    try:
        from PyPDF2 import PdfReader, PdfWriter  # pyright: ignore[reportMissingImports]
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


@role_required(["ADMINISTRADOR", "DIRECTOR"])
def listar_certificados(request: HttpRequest):
    """Vista para listar certificados con opción de generar PDF"""
    
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

def mostrar_registrar_certificado(request: HttpRequest):
    """Mostrar formulario para registrar certificado"""
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

def registrar_certificado(request: HttpRequest):
    """Procesar registro de certificado"""
    from django.contrib import messages
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
