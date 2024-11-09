from django.contrib import admin
from .models import Crianca


class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_de_nascimento',
                    'tamanho_camiseta', 'escola', 'turno', 'telefone_responsavel')
    search_fields = ('nome',)
    list_filter = ('data_de_nascimento',)


admin.site.register(Crianca, CriancaAdmin)
