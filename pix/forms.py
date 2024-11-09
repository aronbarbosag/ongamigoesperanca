# pix/forms.py

from django import forms
from .models import Pagamento

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['nome', 'cpf', 'valor']  # Incluindo o campo cpf