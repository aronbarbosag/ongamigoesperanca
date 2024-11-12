from django.contrib import admin
from .models import Crianca, Atividade, Participacao, Responsavel,Filial, Necessidade_especial


class Filial(admin.ModelAdmin):
    list_display = ('nome_filial')


class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade_calculada','nome_filial',
                    'escola',  'turno', 'rua','nomes_responsaveis','responsavel_grau_de_parentesco' ,'telefone_responsavel')
    search_fields = ('nome',)
    

    list_filter = ('data_de_nascimento',)
    
    list_per_page = (15)

    def idade_calculada(self, obj):
        return obj.idade  # Acessa a propriedade `idade` do modelo
    def nomes_responsaveis(self, obj):
        return obj.nomes_responsaveis 
    def responsavel_grau_de_parentesco(self,obj):
        return obj.responsavel_grau_de_parentesco
    def nome_filial(self,obj):
        return obj.nome_filial
    # Nome que aparecerá no Django Admin
    idade_calculada.short_description = 'Idade'
    nomes_responsaveis.short_description = 'Responsáveis'
    responsavel_grau_de_parentesco.short_description= 'Parentesco'
    nome_filial.short_description = 'Filial'

class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atividade', 'data_inicio', 'data_fim', 'status')
    list_filter = ('atividade', 'status')
    search_fields = ('nome__nome',)
    list_per_page = (15)

class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome','telefone','email','grau_de_parentesco')
    list_per_page = (15)
    search_fields = ('nome','telefone')
    

admin.site.site_header= "Painel de Administração"
admin.site.site_title = "Painel de Administração"
# admin.site.register(Filial)
admin.site.register(Atividade, AtividadeAdmin)
admin.site.register(Crianca, CriancaAdmin)
admin.site.register(Necessidade_especial)
admin.site.register(Participacao, ParticipacaoAdmin)
admin.site.register(Responsavel, ResponsavelAdmin)
