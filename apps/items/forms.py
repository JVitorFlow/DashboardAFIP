from django import forms
from apps.values.models import ShiftData

class ShiftDataForm(forms.ModelForm):
    class Meta:
        model = ShiftData
        fields = [
            'cnes', 'os_number', 'cartao_sus', 'nome_paciente', 'sexo', 
            'raca_etinia', 'idade_paciente', 'data_nascimento', 'data_coleta', 
            'data_liberacao', 'tamanho_lesao', 'caracteristica_lesao', 'localizacao_lesao', 
            'codigo_postal', 'logradouro', 'numero_residencial', 'cidade', 'estado'
        ]
