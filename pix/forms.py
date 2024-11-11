# pix/forms.py

from django import forms
from .models import Pagamento
from django.forms.widgets import NumberInput

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['nome', 'cpf', 'email', 'valor', 'mensagem']

    valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=NumberInput(attrs={'step': '0.01'})
    )