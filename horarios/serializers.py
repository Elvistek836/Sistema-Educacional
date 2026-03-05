from rest_framework import serializers
from .models import Profesor, Curso, Asignatura, AsignaturasProfesor, DisponibilidadProfesor, Horario, Usuario, Historial, Alumnos

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = "__all__"

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = "__all__"

class AsignaturasProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturasProfesor
        fields = "__all__"

class DisponibilidadProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadProfesor
        fields = "__all__"

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = "__all__"

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnos
        fields = "__all__"
