from django import template

register = template.Library()


@register.filter
def readonly_if(value):
    """Retorna readonly se o valor estiver preenchido e não for um marcador de ausência (como 'NI')"""
    if not value:
        return ""  # Permitir edição se for None, vazio, etc.

    value_str = str(value).lower()
    ni_keywords = ["não especificado", "(ni)", "nao especificada"]

    if any(ni_kw in value_str for ni_kw in ni_keywords):
        return (
            ""  # Também permite edição se tiver qualquer indicativo de 'não preenchido'
        )

    return 'readonly style="background-color: #e9ecef;"'  # Caso contrário, bloqueia
