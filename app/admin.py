from django.contrib import admin
from .models import Crianca, Atividade, Participacao


class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_calculada',
                    'escola',  'turno', 'rua', 'telefone_responsavel')
    search_fields = ('nome',)

    list_filter = ('nome', 'data_de_nascimento')

    list_per_page = (10)

    def idade_calculada(self, obj):
        return obj.idade  # Acessa a propriedade `idade` do modelo

    # Nome que aparecerá no Django Admin
    idade_calculada.short_description = 'Idade'


class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atividade', 'data_inicio', 'data_fim', 'status')
    list_filter = ('atividade', 'status')
    list_per_page = (10)


admin.site.register(Crianca, CriancaAdmin)
admin.site.register(Atividade, AtividadeAdmin)
admin.site.register(Participacao, ParticipacaoAdmin)
