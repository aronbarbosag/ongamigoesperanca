from django.contrib import admin
from .models import Crianca, Atividade, Participacao, Responsavel


class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_calculada',
                    'escola',  'turno', 'rua','nomes_responsaveis','responsavel_grau_de_parentesco' ,'telefone_responsavel')
    search_fields = ('nome',)

    list_filter = ('nome', 'data_de_nascimento')
    
    list_per_page = (10)

    def idade_calculada(self, obj):
        return obj.idade  # Acessa a propriedade `idade` do modelo
    def nomes_responsaveis(self, obj):
        return obj.nomes_responsaveis 
    def responsavel_grau_de_parentesco(self,obj):
        return obj.responsavel_grau_de_parentesco
    
    # Nome que aparecerá no Django Admin
    idade_calculada.short_description = 'Idade'
    nomes_responsaveis.short_description = 'Responsáveis'
    responsavel_grau_de_parentesco.short_description= 'Parentesco'

class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atividade', 'data_inicio', 'data_fim', 'status')
    list_filter = ('atividade', 'status')
    list_per_page = (10)

class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome','telefone','email','grau_de_parentesco')


admin.site.site_header= "Painel de Administração ONG Amigo Esperança"
admin.site.site_title = "Painel de Administração"
admin.site.register(Crianca, CriancaAdmin)
admin.site.register(Atividade, AtividadeAdmin)
admin.site.register(Participacao, ParticipacaoAdmin)
admin.site.register(Responsavel)
