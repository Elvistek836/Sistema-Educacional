from django import template

register = template.Library()

@register.filter
def filtrar_registros(hor2, a):
    return [registro for registro in hor2 if registro['bloque'] == a.bloque and registro['dia'] == a.dia and registro['profesor_id'] == a.profesor_id]
