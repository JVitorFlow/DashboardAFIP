from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from apps.utils.choices import Status
from typing import Optional


def check_if_can_change_status(object) -> Optional[PermissionDenied]:
    """
    Verifica se o estado do objeto está na lista de estados inválidos.

    Argumentos:
        objeto (tipo): O objeto cujo estado será verificado.

    Aumenta:
        PermissionDenied: Se o estado do objeto estiver na lista de inválidos
        estados.

    Retorna:
        None ou PermissionDenied: Nenhum se o estado for válido,
        ou uma exceção PermissionDenied se o estado for inválido.
    """
    status = [Status.COMPLETED, Status.ERROR]
    if object.status in status:
        raise PermissionDenied(detail={
            'detail': f"Você não pode modificar o objeto porque está em {status}"
        })


def check_id(*args) -> Optional[ValidationError]:
    """
    Verifica se query_params não estão vazios.

    Argumentos:
        *args: argumentos variáveis ​​a serem verificados.

    Aumenta:
        ValidationError: se algum dos query_params estiver vazio.

    Retorna:
        Nenhum ou ValidationError: Nenhum se query_params forem válidos,
        ou uma exceção ValidationError se algum query_param estiver vazio.
    """
    for id in args:
        if not id:
            raise ValidationError({
                'detail': 'Parâmetros ausentes ou inválidos'
            })


def token_login(function):
    """
    Decorador que atualiza o campo last_login do usuário que faz a solicitação.

    Este decorador pode ser aplicado a visualizações baseadas em classes para atualizar automaticamente
    o campo last_login do usuário toda vez que uma solicitação é feita ao
    vista decorada.

    Argumentos:
        function (chamável): A função de visualização a ser decorada.

    Retorna:
        chamável: uma nova função que envolve a função de visualização original.
        Esta nova função atualiza o campo last_login do usuário e então
        chama a função de visualização original.
    """
    def wrapper(self, request):
        user = request.user
        user.last_login = timezone.now()
        user.save()
        return function(self, request)
    return wrapper
