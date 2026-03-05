from django import forms
from .models import Profesor, Curso, Asignatura, AsignaturasProfesor, DisponibilidadProfesor, Horario, Usuario, Historial, Alumnos, Apoderado, Padre, Actividades, Prestamos, Insumos, Impresiones, ConsejosProfesores, Certificados, Atenciones


#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Profesores-------------------------
#-------------------------------------------------------------------------------------
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'
        widgets = {
            'rut': forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Rut (Ej: 11.111.111-1)'}),
            'nombre':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Nombres'}),
            'apellido':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Apellidos'}),
            'nivel':forms.Select(attrs={'class':'select-control','placeholder':'Nivel de Enseñanza'}),
            'Foto':forms.FileInput(attrs={'class':'form-control','id':'inputGroupFile02'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg','placeholder': 'Email'}),
            }
#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Cursos-----------------------------
#-------------------------------------------------------------------------------------
class CursoForm(forms.ModelForm):
    class Meta:
        model=Curso
        fields='__all__'
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Curso'}),
            }
#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Asignaturas------------------------
#-------------------------------------------------------------------------------------
class AsignaturaForm(forms.ModelForm):
    class Meta:
        model=Asignatura
        fields='__all__'
        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Codigo'}),
            'nombre':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Asignatura'}),
            'nivel':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Nivel de Enseñanza'}),
            'bloques':forms.NumberInput(attrs={'class':'form-control form-control-lg','placeholder':'Cantidad de Bloques'}),
            'curso':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Curso'}),
            }
#-------------------------------------------------------------------------------------
#-------------Personalizacion de Fromulario Especialidad Profesores-------------------
#-------------------------------------------------------------------------------------
class AsignaturasProfesorForm(forms.ModelForm):
    class Meta:
        model=AsignaturasProfesor
        fields='__all__'
        widgets={
            'nombre':forms.Select(attrs={'class':'select-control','placeholder':'Asignatura'}),
            'nivel':forms.TextInput(attrs={'class':'col-form-label','placeholder':'Nivel de Enseñanza'}),
            }
#-------------------------------------------------------------------------------------
#---------------Personalizacion de Fromulario Disponibilidad Profesores---------------
#-------------------------------------------------------------------------------------
class DisponibilidadProfesorForm(forms.ModelForm):
    class Meta:
        model=DisponibilidadProfesor
        fields='__all__'
        widgets={
            'bloque':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Numero de Bloque'}),
            'dia':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Dia'}),
            'estado':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Disponible'}),
            'profesor':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Profesor'}),
        }
#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Horarios---------------------------
#-------------------------------------------------------------------------------------
class HorarioForm(forms.ModelForm):
    class Meta:
        model=Horario
        fields='__all__'
        widgets={
            'bloque':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Numero de Bloque'}),
            'dia':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Dia'}),
            'asignatura':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Asignatura'}),
            'curso':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Curso'}),
            'profesor':forms.Select(attrs={'class':'select-control form-control-lg','placeholder':'Profesor'}),
        }
#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Matriculas-------------------------
#-------------------------------------------------------------------------------------
class AlumnoForm(forms.ModelForm):
    class Meta:
        model=Alumnos
        fields='__all__'
        widgets={
            'matricula':forms.NumberInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:100px'}),
            'curso':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'run':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'nombre':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'apellido_paterno':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'apellido_materno':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'direccion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'comuna':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white'}),
            'procedencia':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'curso_repetido':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white'}),
            'con_quien_vive':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'enfermedad':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'prevision':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white'}),
            'letra_fonasa':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white'}),
            'alimentacion_establecimiento':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white'}),
            'programa_solidario':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white'}),
            'programa':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'locomocion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'fono_locomocion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:120px'}),
            'vive_con':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'emergencia':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'complementarios':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'email':forms.EmailInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'Foto':forms.FileInput(attrs={'class':'form-control','id':'inputGroupFile02','style':'width:400px'}),
            }
#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Apoderados-------------------------
#-------------------------------------------------------------------------------------
class ApoderadoForm(forms.ModelForm):
    class Meta:
        model=Apoderado
        fields='__all__'
        widgets={
            'es_madre':forms.CheckboxInput(attrs={'class':'form-check-input','type':'checkbox','id':'flexSwitchCheckChecked','role':'switch'}),
            'run':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'nombre':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'apellido_paterno':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'apellido_materno':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'fono':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:120px'}),
            'escolaridad':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'ocupacion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 70px; background-color: white;'}),
            'religion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
        }
#-------------------------------------------------------------------------------------
#--------------------Personalizacion de Fromulario Padres-----------------------------
#-------------------------------------------------------------------------------------
class PadreForm(forms.ModelForm):
    class Meta:
        model=Padre
        fields='__all__'
        widgets={
            'run':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'nombre':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:300px'}),
            'apellido_paterno':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'apellido_materno':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'fono':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:120px'}),
            'escolaridad':forms.Select(attrs={'class':'select-control form-control-lg text-dark','style':'background-color: white;width:250px'}),
            'ocupacion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 70px; background-color: white;'}),
            'religion':forms.TextInput(attrs={'class':'form-control form-control-lg text-dark','style':'background-color: white;width:200px'}),
        }
#-------------------------------------------------------------------------------------
#---------------------------------Actividades-----------------------------------------
#-------------------------------------------------------------------------------------
class ActividadesForm(forms.ModelForm):
    FechaHoraPlanificada = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control datetimepicker text-dark',
                'style': 'width: 200px; height: 45px; background-color: white;',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }
        ),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )

    class Meta:
        model = Actividades
        fields = '__all__'
        widgets = {
            'Tipo': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 200px; height: 45px'}),
            'Profesor': forms.Select(attrs={'class': 'select-control form-control-lg', 'readonly': 'readonly'}),
            'Nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 300px; background-color: white'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'Foto1': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Foto2': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Foto3': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'NumeroParticipantesActividad': forms.NumberInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 70px; background-color: white;'}),
        }
#-------------------------------------------------------------------------------------
#---------------------------------Prestamos-------------------------------------------
#-------------------------------------------------------------------------------------
class PrestamosForm(forms.ModelForm):
    FechaHoraDevolucionPrestamo = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control datetimepicker text-dark',
                'style': 'width: 200px; height: 45px; background-color: white;',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }
        ),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )

    class Meta:
        model=Prestamos
        fields='__all__'
        widgets={
            'DetallePrestamo':forms.Textarea(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'FotoPrestamo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'EstadoPrestamo':forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 200px; height: 45px'}),
        }
#-------------------------------------------------------------------------------------
#---------------------------------Impresiones-----------------------------------------
#-------------------------------------------------------------------------------------
class ImpresionesForm(forms.ModelForm):
    FechaHoraUtilizacionImpresion = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control datetimepicker text-dark',
                'style': 'width: 200px; height: 45px; background-color: white;',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }
        ),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )

    class Meta:
        model = Impresiones
        fields = '__all__'
        widgets={
            'CursoImpresion': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 250px; height: 45px'}),
            'AsignaturaImpresion': forms.TextInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'Archivo1Impresion': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Archivo2Impresion': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Archivo3Impresion': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'ObservacionImpresion':forms.Textarea(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'EstadoImpresion': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 200px; height: 45px'}),
        }
#-------------------------------------------------------------------------------------
#---------------------------Consejo de Profesores-------------------------------------
#-------------------------------------------------------------------------------------
class ConsejosProfesoresForm(forms.ModelForm):
    FechaHoraPlanificadaConsejo = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control datetimepicker text-dark',
                'style': 'width: 200px; height: 45px; background-color: white;',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }
        ),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )

    class Meta:
        model = ConsejosProfesores
        fields = '__all__'
        widgets={
            'ComentariosConsejo':forms.TextInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'AcuerdosConsejo':forms.Textarea(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'Archivo1Consejo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Archivo2Consejo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Archivo3Consejo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'NumeroProfesoresConsejo': forms.NumberInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 70px; background-color: white;'}),
        }
#-------------------------------------------------------------------------------------
#---------------------------------Atenciones------------------------------------------
#-------------------------------------------------------------------------------------
class AtencionesForm(forms.ModelForm):
    class Meta:
        model = Atenciones
        fields = '__all__'
        widgets={
            'Tipo': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 450px; height: 45px'}),
            'idMatricula': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 750px; height: 45px'}),
            'Motivo':forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 250px; height: 45px'}),
            'Observaciones':forms.Textarea(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'Foto1Evidencia': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Foto2Evidencia': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Foto3Evidencia': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
        }
#Ordenar el select de los Alumnos Alfabeticamente por el apellido paterno
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí ordenamos los alumnos por el campo apellido_paterno de manera ascendente
        self.fields['idMatricula'].queryset = Alumnos.objects.all().order_by('apellido_paterno')
#-------------------------------------------------------------------------------------
#-----------------------------------Insumos-------------------------------------------
#-------------------------------------------------------------------------------------
class InsumosForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = '__all__'
        widgets={
            'NombreInsumo':forms.TextInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'DetalleInsumo':forms.Textarea(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'StockInsumo': forms.NumberInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 70px; background-color: white;'}),
            'Foto1Insumo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Foto2Insumo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'Foto3Insumo': forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 400px', 'id': 'inputGroupFile02'}),
            'EstadoInsumo': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 200px; height: 45px'}),
        }
#-------------------------------------------------------------------------------------
#---------------------------------Certificados----------------------------------------
#-------------------------------------------------------------------------------------
class CertificadosForm(forms.ModelForm):
    class Meta:
        model = Certificados
        fields = '__all__'
        widgets={
            'idMatricula': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 750px; height: 45px'}),
            'TipoCertificado': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 700px; height: 45px'}),
            'MotivoCertificado':forms.TextInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'LugarPresentacionCertificado':forms.TextInput(attrs={'class': 'form-control form-control-lg text-dark', 'style': 'width: 500px; background-color: white'}),
            'EstadoCertificado': forms.Select(attrs={'class': 'form-select form-select-lg text-dark', 'style': 'width: 200px; height: 45px'}),
        }
#Ordenar el select de los Alumnos Alfabeticamente por el apellido paterno
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí ordenamos los alumnos por el campo apellido_paterno de manera ascendente
        self.fields['idMatricula'].queryset = Alumnos.objects.all().order_by('apellido_paterno')