import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sistema_Educacional.settings')
django.setup()

from django.apps import apps
from django.db import connections
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def migrate_to_mysql():
    print("Iniciando migración de SQLite a MySQL...")
    
    # Crear tablas en MySQL
    print("Creando estructura de tablas en MySQL...")
    call_command('migrate', database='mysql')
    
    # Orden específico para modelos con dependencias
    # Primero migrar modelos base sin dependencias
    base_models = [
        ContentType,
        Permission,
        Group,
        User,
    ]
    
    # Migrar primero los modelos base
    for model in base_models:
        migrate_model(model)
    
    # Obtener todos los modelos de la aplicación
    app_models = [m for m in apps.get_models() if m not in base_models]
    
    # Migrar el resto de los modelos
    for model in app_models:
        migrate_model(model)
    
    print("\nMigración completada exitosamente!")
    print("Recuerda actualizar el archivo settings.py para usar MySQL como base de datos predeterminada.")

def migrate_model(model):
    model_name = f"{model._meta.app_label}.{model._meta.model_name}"
    print(f"Migrando datos para {model_name}...")
    
    # Obtener todos los registros de SQLite
    objects = model.objects.using('default').all()
    
    # Si hay registros para migrar
    if objects.exists():
        count = 0
        # Migrar uno por uno para manejar errores
        for obj in objects:
            try:
                # Crear una copia del objeto para la base de datos MySQL
                obj.pk = obj.pk  # Mantener la misma clave primaria
                obj.save(using='mysql')
                count += 1
            except IntegrityError as e:
                print(f"  - Error al migrar objeto {obj.pk}: {str(e)}")
                continue
        
        print(f"  - {count} registros migrados exitosamente")
    else:
        print(f"  - No hay datos para migrar")

if __name__ == "__main__":
    migrate_to_mysql()