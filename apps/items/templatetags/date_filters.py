from django import template
from datetime import datetime

register = template.Library()

@register.filter
def iso_to_datetime_local(value):
    """Converte ISO 8601 para o formato `datetime-local` do HTML."""
    if not value:
        return ""

    # Se já for um objeto datetime, apenas formata corretamente
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M")

    try:
        # Substituir "Z" por "+00:00" se presente (para fuso horário UTC)
        if isinstance(value, str):
            value = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(value)
            return dt.strftime("%Y-%m-%dT%H:%M")
    except ValueError:
        pass  # Se falhar na conversão, retorna o valor original

    return value  # Retorna o valor original caso não seja possível converter

@register.filter
def iso_to_date(value):
    """Converte ISO 8601 para o formato `date` do HTML."""
    if not value:
        return ""

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    try:
        if isinstance(value, str):
            value = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(value)
            return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    return value  # Retorna o valor original se não for possível converter
