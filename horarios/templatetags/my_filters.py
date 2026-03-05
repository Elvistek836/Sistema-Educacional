from django import template

register = template.Library()

@register.filter
def filtrar_registros(hor2, x):
    resultados = [registro for registro in hor2 if registro['bloque_horario'] == x.bloque_disponible and registro['dia_horario'] == x.dia_disponible and registro['profesor_id'] == x.profesor_id]
    #resultados = [registro for registro in hor2 if registro['profesor_id'] == x.profesor_id]
    return len(resultados)
