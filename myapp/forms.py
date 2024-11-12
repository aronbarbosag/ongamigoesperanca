from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'id':'nome'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id':'email'}))
    comentario = forms.CharField(widget=forms.Textarea(attrs={'id':'email'}), required=True)